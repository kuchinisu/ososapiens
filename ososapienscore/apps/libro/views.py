from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.utils.pagination import LargeSetPagination

class CrearLibroAutomatico(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        pass
    def post(self,request,format=None):
        user = request.user
        data = request.data
        titulo = data.get('titulo')
        autores = data.get('autores')
        proyectos = data.get('proyectos')


