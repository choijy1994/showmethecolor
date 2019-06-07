from django.contrib import admin


from .models import UploadFileModel,ModifiedModel,Cosmetics,Make_up_applied


# Register your models here.

admin.site.register(UploadFileModel)
admin.site.register(ModifiedModel)
admin.site.register(Cosmetics)
admin.site.register(Make_up_applied)