from django.shortcuts import render
from apps.utils.pagination import LargeSetPagination

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

from .models import UserAccount

class UsuariosView(APIView):
    def get(self, request, format=None):
        usuarios = UserAccount.objects.all()

        if usuarios.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(usuarios, request)
            serializer = UserSerializer(results, many=True)

            return paginator.get_paginated_response({'usuarios':serializer.data})
        else:
            return Response({'error':'no hay usuarios registrados en la base de datos'}, status=status.HTTP_404_NOT_FOUND)
        
class UsuarioMatricula(APIView):
    def get(self, request, matricula ,format=None):
        usuarios = UserAccount.objects.filter(matricula=matricula)

        if usuarios.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(usuarios, request)
            serializer = UserSerializer(results, many=True)

            return paginator.get_paginated_response({'usuarios':serializer.data})
        else:
            return Response({'error':'no hay usuarios registrados en la base de datos'}, status=status.HTTP_404_NOT_FOUND)
        
