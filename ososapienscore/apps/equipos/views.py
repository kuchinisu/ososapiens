from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.utils.pagination import LargeSetPagination
from apps.equipos.models import Equipo
from django.utils import timezone
from . serializer import EquipoSerializer
from apps.user.models import UserAccount

from .models import Equipo


class CrearEquipo(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        usuario = request.user
        data = request.data

        nombre = data.get('nombre')
        usuarios = data.get('usuarios', [])

        nuevo_equipo = Equipo(nombre=nombre) 
        nuevo_equipo.save()

        for user_slug in usuarios:
            try:
                us = get_object_or_404(UserAccount, slug=user_slug)
                nuevo_equipo.integrantes.add(us)
            except:
                return Response({'error': f'Usuario con slug {user_slug} no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        nuevo_equipo.integrantes.add(usuario)

        return Response({'mensaje': f'Nuevo equipo con el nombre {nombre} creado'}, status=status.HTTP_201_CREATED)

class EquiposView(APIView):
    def get(self,request, format=None):
        
        equipos = Equipo.objects.all()
        
        if equipos.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(equipos, request)
            serializer = EquipoSerializer(results, many=True)

            return paginator.get_paginated_response({'equipos':serializer.data})
        else:
            return Response({'error':'no hay equipos registrados en la base de datos'}, status=status.HTTP_404_NOT_FOUND)   

class EquipoSlug(APIView):
    def get(self, request, slug, format=None):
        equipos = Equipo.objects.filter(slug=slug)
        
        if equipos.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(equipos, request)
            serializer = EquipoSerializer(results, many=True)

            return paginator.get_paginated_response({'equipo':serializer.data})
        else:
            return Response({'error':'el equipo no existe o fue eliminado'}, status=status.HTTP_404_NOT_FOUND)

class EquiposNombre(APIView):
    def get(self, request, nombre, format=None):
        equipos = Equipo.objects.filter(nombre=nombre)
        
        if equipos.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(equipos, request)
            serializer = EquipoSerializer(results, many=True)

            return paginator.get_paginated_response({'equipo':serializer.data})
        else:
            return Response({'error':f'no hay resultados para "{nombre}"'}, status=status.HTTP_404_NOT_FOUND)


