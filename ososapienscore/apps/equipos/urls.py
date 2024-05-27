from django.urls import path
from .views import *

urlpatterns = [
    path('crear_equipo/', CrearEquipo.as_view()),
]
