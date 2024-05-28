from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from apps.utils.pagination import LargeSetPagination
from apps.equipos.models import Equipo
from django.utils import timezone

from .serializers import (DisciplinaSerializer, ProyectoSerializer, 
                          AvanceSerializer, ArchivoSerializer)
from apps.user.models import UserAccount

from .models import (Disciplina, DisciplinasEspecificas, Proyecto, Avance, Archivo)

#Discpiplina
class CrearDisciplina(APIView):
    def get(self, request, format=None):
        pass
    def post(self, request, format=None):
        data = request.data
        nombre = data.get('nombre')

        if Disciplina.objects.filter(nombre=nombre).exists():
            return Response({'no autorizo':'disciplina con el mismo nombre ya existente'}, status=status.HTTP_409_CONFLICT)
        else:
            nueva_disciplina = Disciplina(nombre=nombre)
            nueva_disciplina.save()

            return Response({"mensaje":f"nueva disciplina con el nombre {nombre} creada"}, status=status.HTTP_201_CREATED)

class DisciplinasView(APIView):
    def get(self, request, format=None):
        disciplinas = Disciplina.objects.all()

        if not disciplinas.exists():
            return Response({"error":"no existen disciplinas en la base de datos"}, status=status.HTTP_404_NOT_FOUND)
        else:
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(disciplinas, request)
            serializer = DisciplinaSerializer(results, many=True)

            return paginator.get_paginated_response({"disciplinas":serializer.data})
        

class DisciplinasPorNombreView(APIView):
    def get(self, request, nombre, format=None):
        disciplinas = Disciplina.objects.filter(nombre=nombre)

        if not disciplinas.exists():
            return Response({"error":f"no hay resultados para {nombre}"}, status=status.HTTP_404_NOT_FOUND)
        else:
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(disciplinas, request)
            serializer = DisciplinaSerializer(results, many=True)

            return paginator.get_paginated_response({"disciplinas_por_nombre":serializer.data})
        
class CrearDisciplinasEspecificas(APIView):
    def get(self, request, disciplina, nombre, format=None):
        pass
    def post(self, request, disciplina_nombre, nombre, format=None):
        data = request.data
        disciplina_nombre = data.get('disciplina_nombre')
        nombre = data.get('nombre')
        disciplina = Disciplina.objects.filter(nombre=disciplina_nombre)
        mensaje_extra = ''
        if not disciplina.exists():
            disciplina = Disciplina(nombre=disciplina_nombre)
            disciplina.save()

            mensaje_extra += f'y nueva disciplina con el nombre {disciplina_nombre} creada'

        else: disciplina = disciplina.last()

        if not DisciplinasEspecificas.objects.filter(disciplina=disciplina, nombre=nombre):
            nueva_disciplina_especifica = DisciplinasEspecificas(disciplina=disciplina, nombre=nombre)
            nueva_disciplina_especifica.save()
            
            return Response({"mensaje":f"nueva disciplina especifica con el nombre {nombre} creada {mensaje_extra}"}, status=status.HTTP_201_CREATED)
        else: 
            return Response({"no autorizo":f'disciplina especifica con el nombre {nombre} ya existente'},status=status.HTTP_409_CONFLICT)

class DisciplinasEspecificasView(APIView):
    def get(self, request, disciplina, format=None):
        disciplina = get_object_or_404(Disciplina, nombre=disciplina)
        dis_esp = DisciplinasEspecificas.objects.filter(disciplina=disciplina)
        if dis_esp.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(dis_esp, request)
            serializer = DisciplinaSerializer(results, many=True)

            return paginator.get_paginated_response({'disciplinas_especificas':serializer.data})
        else:
            return Response({'error':f'no hay subdiciplinas a partir de {disciplina.nombre}'}, status=status.HTTP_404_NOT_FOUND)

class DisciplinasEspecificasPorNombreView(APIView):
    def get(self, request, disciplina, nombre, format=None):
        disciplina = get_object_or_404(Disciplina, nombre=disciplina)
        dis_esp = DisciplinasEspecificas.objects.filter(disciplina=disciplina, nombre=nombre)
        if dis_esp.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(dis_esp, request)
            serializer = DisciplinaSerializer(results, many=True)

            return paginator.get_paginated_response({'disciplinas_especificas_por_nombre':serializer.data})
        else:
            return Response({'error':f'no hay resultados para {nombre}'}, status=status.HTTP_404_NOT_FOUND)


#proyecto
class CrearProyecto(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        data = request.data

        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        disciplina_n = data.get('disciplina')
        fecha_de_finalizacion_fija = data.get('fecha_de_finalizacion_fija')
        fecha_de_finalizacion = data.get('fecha_de_finalizacion')
        publico = data.get('publico')
        habilitar_api = data.get('habilitar_api')
        diciplinas_especificas = data.get('diciplinas_especificas', [])
        equipo_slug = data.get('equipo')

        equipo = get_object_or_404(Equipo, slug=equipo_slug)
        disciplina = get_object_or_404(Disciplina, nombre=disciplina_n)

        if not user in equipo.integrantes.all():
            return Response({"error": "Necesitas ser integrante del equipo al que intentas atribuir el proyecto"}, status=status.HTTP_401_UNAUTHORIZED)

        nuevo_proyecto = Proyecto(
            nombre=nombre,
            descripcion=descripcion,
            disciplina=disciplina,
            fecha_de_finalizacion_fija=fecha_de_finalizacion_fija,
            fecha_de_finalizacion=fecha_de_finalizacion or timezone.now().date(),
            equipo=equipo,
            publico=publico,
            habilitar_api=habilitar_api,
        )
        nuevo_proyecto.save()

        for disciplina_especifica in diciplinas_especificas:
            d_esp, created = DisciplinasEspecificas.objects.get_or_create(nombre=disciplina_especifica)
            nuevo_proyecto.diciplinas_especificas.add(d_esp)
        
        return Response({'mensaje': f'Nuevo proyecto con el nombre {nombre} del equipo ({equipo.slug})-{equipo.nombre} creado correctamente'}, status=status.HTTP_201_CREATED)

class ProyectoView(APIView):
    def get(self, request, format = None):
        proyectos = Proyecto.objects.all()
        if proyectos.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(proyectos, request)
            serializer = ProyectoSerializer(results, many=True)

            return Response({'proyectos':serializer.data})
        else:
            return Response({'error':'no hay proyectos en la base de datos'}, status=status.HTTP_404_NOT_FOUND)
        

class ProyectoSlugView(APIView):
    def get(self, request, slug, format = None):
        proyectos = Proyecto.objects.filter(slug=slug)
        if proyectos.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(proyectos, request)
            serializer = ProyectoSerializer(results, many=True)

            return Response({'proyecto':serializer.data})
        else:
            return Response({'error':'el proyecto fue eliminado o no existe'}, status=status.HTTP_404_NOT_FOUND)
        

class ProyectosPorNombreView(APIView):
    def get(self, request, nombre, format = None):
        proyectos = Proyecto.objects.filter(nombre=nombre, publico=True)
        if proyectos.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(proyectos, request)
            serializer = ProyectoSerializer(results, many=True)

            return Response({'proyectos_por_nombre':serializer.data})
        else:
            return Response({'error':f'no hay resultados para {nombre}'}, status=status.HTTP_404_NOT_FOUND)
        
class ProyectosPorEquipoView(APIView):
    def get(self, request, equipo, format = None):
        equipo=get_object_or_404(Equipo, slug=equipo)
        proyectos = Proyecto.objects.filter(equipo=equipo, publico=True)
        if proyectos.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(proyectos, request)
            serializer = ProyectoSerializer(results, many=True)

            return Response({'proyectos_de_equipo':serializer.data})
        else:
            return Response({'error':'el equipo aún no tiene ningún proyecto disponible'}, status=status.HTTP_404_NOT_FOUND)
        
#Avances
class CrearAvance(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        pass
    def post(self, request, format=None):
        user = request.user
        data = request.data
        
        proyecto_slug = data.get('proyecto')

        responsables = data.get('responsables')
        titulo = data.get('titulo')
        descripcion = data.get('descripcion')

        proyecto = get_object_or_404(Proyecto, slug=proyecto_slug)
        equipo = proyecto.equipo.integrantes.all()

        if user in equipo:
            nuevo_avance = Avance(
                titulo=titulo,
                proyecto=proyecto,
                descripcion=descripcion,    
            )
           

            for responsable_matricula in responsables:
                responsable = get_object_or_404(UserAccount, matricula=responsable_matricula)
                if responsable in equipo.all():
                    nuevo_avance.responsable.add(responsable)

class AvancesView(APIView):
    def get(self, request, proyecto, format=None):
        
        proyecto=get_object_or_404(Proyecto, slug = proyecto, publico=True)
        
        avances = Avance.objects.filter(proyecto = proyecto)

        if avances.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(avances, request)
            serializer = AvanceSerializer(results, many=True)

            return Response({'avances':serializer.data})
        else:
            return Response({'error':'el proyecto aún no tiene avances'})
    
#archivo
class CrearArchivo(APIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, format=None):
        pass
    def post(self, request, format=None):
        user = request.user
        data = request.data()
        
        avance_slug = data.get('avance')
        avance = get_object_or_404(Avance, slug=avance_slug)
        equipo = avance.proyecto.equipo.integrantes.all()

        if user in equipo:
            archivo = request.FILES.get("archivo")
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')
            subcarpetas = data.get('subcarpetas')

            nuevo_archivo = Archivo(
                nombre=nombre,
                descripcion=descripcion,
                subcarpetas=subcarpetas,
                avance=avance,
            )
            nuevo_archivo.archivo = archivo

            nuevo_archivo.save()

            return Response({'mensaje':'archivo subido correctamente'}, status=status.HTTP_201_CREATED)

class ArchivosView(APIView):
    def get(self, request, avance, format=None):
        avance = get_object_or_404(Avance, slug=avance)
        archivos = Archivo.objects.filter(avance=avance)
        
        if archivos.exists():
            paginator = LargeSetPagination()
            results = paginator.paginate_queryset(archivos, request)
            serializer = ArchivoSerializer(results, many=True)

            return paginator.get_paginated_response({'archivos':serializer.data})
        else:
            return Response({'error':'no hay archivos disponibles'}, status=status.HTTP_404_NOT_FOUND)
