from django.urls import path
from .views import (CrearEquipo, EquiposView,EquipoSlug, EquiposNombre)

urlpatterns = [
    path('crear/equipo/', CrearEquipo.as_view()),
    
    path('lista/equipo/', EquiposView.as_view()),
    path('lista/equipo/slug/<slug>/', EquipoSlug.as_view()),
    path('lista/equipos/nombre/<nombre>/', EquiposNombre.as_view()),
]
