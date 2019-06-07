from django.db import models
import os
import cv2
import math
import numpy as np
from capstone.settings import MEDIA_ROOT
from django.core.files import File
from .ApplyMakeup import ApplyMakeup
from .WhiteBalance import WhiteBalance
from django.core.exceptions import ValidationError

def path_and_rename(instance,filename):
    upload_to = 'beforeimages/'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.pk,ext)
    return os.path.join(upload_to,filename)

def modify_and_rename(instance,filename):
   upload_to = 'afterimages/'
   ext = filename.split('.')[-1]
   filename = '{}.{}'.format(instance.pk,ext)
   return os.path.join(upload_to,filename)

def Applied_and_rename(instance,filename):
    upload_to = 'output/'
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.pk,ext)
    return os.path.join(upload_to,filename)


class UploadFileModel(models.Model):
    name = models.CharField(max_length=255,default='',unique = True,primary_key = True)
    file = models.ImageField(upload_to=path_and_rename,  null=True, blank=True)
    checked = models.BooleanField(default=0)
    tone = models.CharField(max_length=10,default='')


    def clean(self):
        if UploadFileModel.objects.filter(name=self.name).exists():
            raise ValidationError("이름이 이미 존재합니다")


    def save(self,*args,**kwargs):
        super(UploadFileModel,self).save()
        f = File(self.file)
        new_name = self.name

        new_model = ModifiedModel(name=new_name,file=f)
        new_model.save()
        return self.name



class ModifiedModel(models.Model):
    name = models.CharField(max_length=255,default='',primary_key=True,unique=True)
    file = models.ImageField(upload_to = modify_and_rename)
    checked = models.BooleanField(default=0)
    tone = models.CharField(max_length=10, default='')
    def save(self,*args,**kwargs):
        super(ModifiedModel,self).save()
        filename = os.path.join(MEDIA_ROOT,self.file.name)
        WhiteBalance(filename)

    def __str__(self):
        return self.name

class Make_up_applied(models.Model):
    name = models.CharField(max_length=255,default='',primary_key = True)
    file = models.ImageField(upload_to =Applied_and_rename )



class Cosmetics(models.Model):
    name = models.CharField(max_length=50,default = '',primary_key=True,unique = True)
    brand = models.CharField(max_length=50,default='')
    season = models.CharField(max_length=10,default='')
    R = models.IntegerField()
    G = models.IntegerField()
    B = models.IntegerField()






