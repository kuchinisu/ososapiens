from django.db import models

from apps.user.models import UserAccount
from apps.investigacion.models import Proyecto

class Libro(models.Model):
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    slug = models.SlugField(unique=True)
    proyectos = models.ManyToManyField(Proyecto, related_name='proyectos_libro', blank=True)
    autores = models.ManyToManyField(UserAccount, related_name='autores_libro')

class Pagina(models.Model):
    superior_de_pagina = models.TextField(blank=True)
    titulo = models.CharField(blank=True, max_length=255)
    numero = models.IntegerField(blank=True, default=1)

    contenido = models.TextField(blank=True)
    pie_de_pagina = models.TextField(blank=True)

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)

    def get_libro(self):
        if self.libro:
            return self.libro.slug