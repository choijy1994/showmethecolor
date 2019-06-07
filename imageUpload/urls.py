from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.init,name='init'),
    path('image_upload',views.upload_file,name = 'image_upload'),
    path('choice/<name>/',views.choice.as_view(),name='choice'),
    path('choice/<name>/success',views.success,name='success'),
    path('choice/<name>/make_up',views.make_up,name='make_up'),
    path('choice/<name>/apply_makeup',views.apply_makeup,name='apply_makeup'),


]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)