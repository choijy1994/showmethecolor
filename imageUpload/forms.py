from django import forms
from .models import *


MY_CHOICES = (
    (11, '업로드 이미지'),
    (12, '수정된 이미지'),
)

class UploadFileForm(forms.ModelForm):

    class Meta:
        model = UploadFileModel
        fields = ['name','file']

    def __init__(self,*args,**kwargs):
        super(UploadFileForm,self).__init__(*args,**kwargs)
        self.fields['file'].required = False
        self.fields['name'].required = True



