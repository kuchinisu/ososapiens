from rest_framework import serializers
from .models import (Disciplina, DisciplinasEspecificas, Proyecto, Avance, Archivo)

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields=[
            'nombre'
        ]

class DisciplinasEspecificas:
    disciplina = serializers.ModelField(source='get_disciplina')
    class Meta:
        model = DisciplinasEspecificas
        fields=[
            'nombre',
            'disciplina',
        ]

class ProyectoSerializer(serializers.ModelSerializer):
    disciplina = serializers.ModelField(source='get_disciplina')
    equipo = serializers.ModelField(source='get_equipo')

    class Meta:
        model = Proyecto
        fields = [
            'nombre',
            'descripcion',
            'fecha',
            'disciplina',
            'fecha_de_finalizacion_fija',
            'fecha_de_finalizacion',
            'equipo',
            'publico',
            'habilitar_api',
            'diciplinas_especificas',
            'slug',
        ]
        
class AvanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avance
        fields = [
            'fecha',
            'responsable',
            'titulo',
            'descripcion',
            'proyecto',
            'slug',

        ]
class ArchivoSerializer(serializers.ModelSerializer):
    archivo = serializers.ModelField(source='get_archivo')
    avance = serializers.ModelField(source='get_avance')
    class Meta:
        model = Archivo
        fields = [
            'archivo',
            'avance',
        ]