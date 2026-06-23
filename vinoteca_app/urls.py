from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('nosotros/', views.nosotros, name='nosotros'),
    path('productos/', views.productos, name='productos'),
    path('contacto/', views.contacto, name='contacto'),
]