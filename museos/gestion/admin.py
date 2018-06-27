from django.contrib import admin

# Register your models here.

from gestion.models import Museo
admin.site.register(Museo)
from gestion.models import PaginaUsuario
admin.site.register(PaginaUsuario)
from gestion.models import Comentarios
admin.site.register(Comentarios)
from gestion.models import Elegidos
admin.site.register(Elegidos)

