from django.urls import path
from . import views

from . import create_superuser

urlpatterns = [
    path('', views.home, name='home'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('productos/', views.productos, name='productos'),
    path('contacto/', views.contacto, name='contacto'),

    path('registro/', views.registro_view, name='registro'),
    path('validar-cuenta/', views.validar_cuenta_view, name='validar_cuenta'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('api/vinos-externos/', views.ListaVinosExternosAPIView.as_view(), name='api_vinos_externos'),
]