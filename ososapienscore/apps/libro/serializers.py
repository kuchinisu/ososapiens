from rest_framework import serializers
from .models import Libro, Pagina

class LibroSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Libro 
        fields = [
            'titulo',
            'autores',
            'slug',
            'proyectos',

        ]
class PaginasSerializer(serializers.ModelSerializer):
    libro = serializers.ModelField(source='get_libro')
    class Meta:
        model=Pagina
        fields=[
            'superior_de_pagina',
            'titulo',
            'numero',
            'contenido',
            'pie_de_pagina',
            'libro',
        ]