# DigitSoftProyecto/urls.py (CORREGIDO PARA MODELOS CONSOLIDADOS)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DigitSoft.urls')),
    path('administrador/', include('administrador.urls')),
    path('autenticacion/', include('autenticacion.urls')),
]

# Servir archivos de media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
