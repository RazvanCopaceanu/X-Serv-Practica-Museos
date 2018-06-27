from django.contrib import admin
from aparcamientos.models import Aparcamiento
from aparcamientos.models import PaginaUsuario
from aparcamientos.models import Comentarios
from aparcamientos.models import Elegidos


# Register your models here.

admin.site.register(Aparcamiento)
admin.site.register(PaginaUsuario)
admin.site.register(Comentarios)
admin.site.register(Elegidos)

