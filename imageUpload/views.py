from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.views.generic import TemplateView
from .detect_face import DetectFace
from .dominant_colors import DominantColors
from .ApplyMakeup import ApplyMakeup
from .getjson import GetJson
from .tone_analysis import ToneAnalysis
from colormath.color_objects import LabColor, sRGBColor, HSVColor
from colormath.color_conversions import convert_color
import operator

# Create your views here.
def init(request):
    return render(request, 'init.html')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        name = request.POST.get('name')
        if form.is_valid():
            form.save()
            return redirect('choice/'+name)
    else:
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})

class choice(TemplateView):
    template_name = 'choice.html'

    def get_context_data(self,**kwargs):
        context = super(choice,self).get_context_data(**kwargs)

        if 'name' in self.kwargs:
            context['modelone'] = UploadFileModel.objects.get(name=self.kwargs['name'])
            context['modeltwo'] = ModifiedModel.objects.get(name=self.kwargs['name'])
        return context

def success(request,**kwargs):
    if request.method=='POST':
        t = request.POST['choices']
        if t == 'uploaded':
            Pic = UploadFileModel.objects.get(name = kwargs['name'])
            UploadFileModel.objects.filter(name=kwargs['name']).update(checked=True)
            image = os.path.join(MEDIA_ROOT,Pic.file.name)

        elif t == 'modified':
            Pic = ModifiedModel.objects.get(name = kwargs['name'])
            ModifiedModel.objects.filter(name=kwargs['name']).update(checked=True)
            image = os.path.join(MEDIA_ROOT ,Pic.file.name)


    predictor = os.path.join(MEDIA_ROOT, "shape_predictor_68_face_landmarks.dat")
    file = File(Pic.file)

    applied = Make_up_applied.objects.create(name=kwargs['name'], file=file)
    seasons = ['spring', 'summer', 'fall', 'winter']
    tone_analysis = ToneAnalysis()
    my_tone = ''

    a = [30, 20, 5]  # 가중치
    for j in range(4):  # j = season

        df = DetectFace(predictor, image)
            # Try: Extract left eye part
        l_eye = df.extract_face_part(df.left_eye)
            # Try: Extract left eyebrow part
        l_eyebrow = df.extract_face_part(df.left_eyebrow)
            # Try : Extract cheek part
        l_cheek = df.cheek_img[0]

            # Create an DominantColors instance on left cheek image
        clusters = 5
        lc_dc = DominantColors(l_cheek, clusters)
        lc_dc.dominantColors()
        lc_colors = lc_dc.plotHistogram()

        leb_dc = DominantColors(l_eyebrow, clusters)
        leb_dc.dominantColors()
        leb_colors = leb_dc.plotHistogram()

        le_dc = DominantColors(l_eye, clusters)
        le_dc.dominantColors()
        le_colors = le_dc.plotHistogram()

        cy_rgb = [lc_colors[0], leb_colors[0], le_colors[0]]
        lab_b = []  # skin, eyebr, eye
        hsv_s = []  # skin, eyebr, eye
        for color in cy_rgb:
            rgb = sRGBColor(color[0], color[1], color[2], is_upscaled=True)
            lab = convert_color(rgb, LabColor, through_rgb_type=sRGBColor)
            lab_b.append(float(format(lab.lab_b, ".2f")))
            hsv = convert_color(rgb, HSVColor, through_rgb_type=sRGBColor)
            hsv_s.append(float(format(hsv.hsv_s * 100, ".2f")))

        if (tone_analysis.is_warm(lab_b, a)):
            if (tone_analysis.is_spr(hsv_s, a)):
                my_tone="봄웜"
            else:
                my_tone="가을웜"
        else:
            if (tone_analysis.is_smr(hsv_s, a)):
                my_tone="여름쿨"
            else:
                my_tone="겨울쿨"
        UploadFileModel.objects.filter(name=kwargs['name']).update(tone=my_tone)
        ModifiedModel.objects.filter(name=kwargs['name']).update(tone=my_tone)
        context={
            'pic':Pic,
            'my_tone':my_tone,
        }
    return render(request, 'success.html',context)


def make_up(request,**kwargs):
    name = kwargs['name']
    ul_checked = UploadFileModel.objects.get(name=name).checked
    mo_checked = ModifiedModel.objects.get(name=name).checked

    if ul_checked ==0:
        Pic = ModifiedModel.objects.get(name=name)
    elif mo_checked==0:
        Pic = UploadFileModel.objects.get(name=name)

    makeup =Make_up_applied.objects.get(name=Pic.name)
    cosmetic = Cosmetics.objects.filter(season=Pic.tone)
    context={
        'pic':Pic,
        'applied':makeup,
        'cosmetics':cosmetic,
    }
    return render(request,'make_up.html',context)

def apply_makeup(request,**kwargs):
    if request.method=='POST':
        t = request.POST['lip']
        cosmetics = Cosmetics.objects.get(name=t)

    name = kwargs['name']
    ul_checked = UploadFileModel.objects.get(name=name).checked
    mo_checked = ModifiedModel.objects.get(name=name).checked

    if ul_checked == 0:
        Pic = ModifiedModel.objects.get(name=name)
    elif mo_checked == 0:
        Pic = UploadFileModel.objects.get(name=name)



    predictor = os.path.join(MEDIA_ROOT, "shape_predictor_68_face_landmarks.dat")


    Make_up_applied.objects.filter(name=Pic.name).delete()
    file = File(Pic.file)
    applied = Make_up_applied.objects.create(name=kwargs['name'], file=file)


    image = os.path.join(MEDIA_ROOT,applied.file.name)

    AM = ApplyMakeup(predictor,image)
    AM.apply_lipstick(cosmetics.R,cosmetics.G,cosmetics.B)
    context = {
        'pic':Pic,
        'cosmetics':cosmetics,
        'applied':applied,
    }

    return render(request,'apply_makeup.html',context)











