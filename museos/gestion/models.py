from django.db import models
from django.contrib.auth.models import User


class Museo(models.Model):
    nombre = models.CharField(max_length=64, default="")
    descripcion = models.TextField(default="")
    accesibilidad = models.IntegerField(default=0)
    url = models.URLField(max_length=300, default="")
    localidad = models.CharField(max_length=200, default="")
    nombre_via = models.CharField(max_length=200, default="")
    clase_vial = models.CharField(max_length=200, default="")
    provincia = models.CharField(max_length=200, default="")
    codigo_postal = models.CharField(max_length=200, default="")
    barrio = models.CharField(max_length=200, default="")
    distrito = models.CharField(max_length=200, default="")
    num = models.CharField(max_length=200, default="")
    coord_x = models.CharField(max_length=200, default="")
    coord_y= models.CharField(max_length=200, default="")
    latitud = models.CharField(max_length=200, default="")
    longitud = models.CharField(max_length=200, default="")
    telefono = models.CharField(max_length=200, default="")
    email = models.URLField(max_length=200, default="")
    n_coment = models.IntegerField(default=0)
    def __str__(self):
        return(self.nombre)
            


class PaginaUsuario(models.Model):
    usuario = models.OneToOneField(User)
    titulo = models.CharField(max_length=200, default="")
    color = models.CharField(max_length=200, default="")
    size = models.CharField(max_length=200, default="")

class Comentarios(models.Model):
    museo = models.ForeignKey(Museo)
    texto = models.TextField(max_length=300, default="")
    def __str__(self):
        return "Comentario para: " + self.museo.nombre + "==>" + self.texto


class Elegidos(models.Model):
    museo = models.ForeignKey(Museo)
    usuario = models.ForeignKey(User)
    fecha = models.DateTimeField()