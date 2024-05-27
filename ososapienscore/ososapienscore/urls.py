from django.contrib import admin
from django.urls import path, re_path, include

from django.views.generic import TemplateView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/', include('djoser.social.urls')),

    path('equipo/', include('apps.equipos.urls')),
    path('investigacion/', include('apps.investigacion.urls')),

    path('admin/', admin.site.urls),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


