from django.db import models
from apps.user.models import UserAccount
from django.utils import timezone

class Equipo(models.Model):
    nombre = models.CharField(max_length=50)
    fecha = models.TimeField(default=timezone.now())
    slug = models.SlugField(default=1, unique=True)
    integrantes = models.ManyToManyField(UserAccount)
    

    def save(self,*args, **kwargs):
        equipos = Equipo.objects.all()
        if equipos.exists():
            equipo = equipos.filter('slug').last()
            slug = str(int(equipo.slug) + 1)

            self.slug=slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre}-({self.slug})'
