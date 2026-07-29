from django.urls import path
from . import views

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

    path('panel-admin/consultas/', views.panel_consultas, name='panel_consultas'),
    path('panel-admin/consultas/<int:pk>/editar/', views.editar_consulta, name='editar_consulta'),
    path('panel-admin/consultas/<int:pk>/eliminar/', views.eliminar_consulta, name='eliminar_consulta'),

    path('olvide-password/', views.olvide_password_view, name='olvide_password'),
    path('reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]