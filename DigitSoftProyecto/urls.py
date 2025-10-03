# DigitSoftProyecto/urls.py (CORRECTO)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('DigitSoft.urls')),
    path('administrador/', include('administrador.urls')),
]