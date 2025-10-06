from django.urls import path, include
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pagina-principal/', views.pagina_principal, name='pagina_principal'),
    path('tienda/', views.tienda, name='tienda'),
    path('portafolio/', views.portafolio, name='portafolio'),
    path('servicios/', views.servicios, name='servicios'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('contacto/', views.contacto, name='contacto'),
]
