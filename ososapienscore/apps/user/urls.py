from django.urls import path
from .views import UsuarioMatricula, UsuariosView



urlpatterns = [
    path('usuarios/', UsuariosView.as_view()),
    path('usuarios/<matricula>/', UsuarioMatricula.as_view()),
    
]
