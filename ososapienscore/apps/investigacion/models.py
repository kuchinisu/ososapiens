from django.db import models
from django.utils import timezone
from apps.equipos.models import Equipo
from apps.user.models import UserAccount
import uuid
import os

def path_dir(instance, filename):
    ext = filename.split('.')[-1]
    nombre_archivo = f"{uuid.uuid4()}.{ext}"
    categoria = instance.avance.proyecto.disciplina.nombre
    proyecto = instance.avance.proyecto.nombre
    avance = instance.avance.titulo  
    nombre = instance.nombre
    equipo = f"{instance.avance.proyecto.equipo.nombre}-{instance.avance.proyecto.equipo.slug}"

    subcarpetas = instance.subcarpetas if instance.subcarpetas else ""
    ruta_completa = os.path.join(categoria, equipo, proyecto, avance, nombre, subcarpetas, nombre_archivo)
    
    print(ruta_completa)  
    
    return ruta_completa

class Disciplina(models.Model):
    nombre=models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class DisciplinasEspecificas(models.Model):
    nombre = models.CharField(max_length=250)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='subdisciplina_dela_disciplina') 

    def __str__(self):
        return self.nombre 
    
    def get_disciplina(self):
        if self.disciplina:
            return self.disciplina.nombre

class Proyecto(models.Model):
    nombre = models.CharField(max_length=250)
    descripcion = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='proyecto_dela_disciplina')

    fecha_de_finalizacion_fija = models.BooleanField(default=False)
    fecha_de_finalizacion = models.DateField(default=timezone.now)
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='proyecto_del_equipo')
    publico = models.BooleanField(default=True)
    habilitar_api = models.BooleanField(default=True)
    diciplinas_especificas = models.ManyToManyField(DisciplinasEspecificas, blank=True)

    slug = models.SlugField(unique=True, default='1')

    def save(self, *args, **kwargs):
        if not self.id:
            ultimo_proyecto = Proyecto.objects.order_by('-id').first()
            if ultimo_proyecto:
                ultimo_id = int(ultimo_proyecto.slug)
                self.slug = str(ultimo_id + 1)
        super(Proyecto, self).save(*args, **kwargs)
    def __str__(self):
        return f'{self.nombre}-({self.slug}) equipo:{self.equipo.nombre}-({self.equipo.slug})'
    
    def get_disciplina(self):
        if self.disciplina:
            return self.disciplina.nombre
    def get_equipo(self):
        if self.equipo:
            return self.equipo.nombre
        return ''
    

class Avance(models.Model):
    fecha = models.DateTimeField(default=timezone.now)
    responsable = models.ManyToManyField(UserAccount)
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)

    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE, related_name='avance_del_proyecto')
    slug = models.SlugField(unique=True, default='1')
    
    def save(self, *args, **kwargs):
        avances = Avance.objects.all()

        if avances.exists():
            avance = avances.filter('slug').last()
            slug = str(int(avance.slug) + 1)
            self.slug = slug
        super().save(*args, **kwargs)

    def get_proyecto(self):
        if self.proyecto:
            return self.proyecto.slug


        
class Archivo(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    subcarpetas = models.CharField(blank=True,max_length=250)
    archivo = models.FileField(upload_to=path_dir)
    avance = models.ForeignKey(Avance, on_delete=models.CASCADE, related_name='archivo_del_avance')
    slug = models.SlugField(unique=True, default='1')
    
    def save(self, *args, **kwargs):
        archivos = Archivo.objects.all()

        if archivos.exists():
            archivo = archivos.filter('slug').last()
            slug = str(int(archivo.slug) + 1)
            self.slug = slug
        super().save(*args, **kwargs)

    def get_archivo(self):
        if self.archivo:
            return self.archivo.url
        return ''
    def get_avance(self):
        if self.avance:
            return self.avance.slug
