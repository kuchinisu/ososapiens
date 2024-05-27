from django.urls import path
from .views import *

urlpatterns = [
    path('crear/disciplina/', CrearDisciplina.as_view()),
    path('crear/disciplinas_especificas/', CrearDisciplinasEspecificas.as_view()),
    path('crear/proyecto/', CrearProyecto.as_view()),
    path('crear/avance/', CrearAvance.as_view()),
    path('crear/arcvhivo/', CrearArchivo.as_view()),

    path('lista/disciplina/', DisciplinasView.as_view()),
    path('lista/disciplina/<nombre>/', DisciplinasPorNombreView.as_view()),
    path('lista/disciplinas_especificas/', DisciplinasEspecificasView.as_view()),
    path('lista/disciplinas_especificas/<nombre>/', DisciplinasEspecificasPorNombreView.as_view()),
    path('lista/proyecto/', ProyectoView.as_view()),
    path('lista/proyecto/nombre/<nombre>/', ProyectosPorNombreView.as_view()),
    path('lista/proyecto/slug/<slug>/', ProyectoSlugView.as_view()),
    path('lista/proyecto/equipo/<equipo>/', ProyectosPorEquipoView.as_view()),
    path('lista/avance/proyecto/<proyecto>/', AvancesView.as_view()),
    path('lista/arcvhivo/avance/<avance>/', ArchivosView.as_view()),

]
