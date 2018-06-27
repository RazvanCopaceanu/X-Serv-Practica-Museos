from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from gestion.models import Museo
from gestion.models import PaginaUsuario
from gestion.models import Comentarios
from gestion.models import Elegidos
from bs4 import BeautifulSoup
import urllib
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib.auth import authenticate, login, logout
import datetime

#https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full
def parser():
    link = 'https://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31ca'
    link += 'e77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&format=xml&file'
    link += '=0&filename=201132-0-museos&mgmtid=118f2fdbecc63410VgnVCM1000000b205a0aRCRD&preview=full'
    fil = urllib.request.urlopen(link)
    soup = BeautifulSoup(fil, 'html.parser')
    for contenido in soup.findAll('contenido'):
        record = Museo()
        for atributo in contenido.findAll('atributo'):
            if atributo.attrs["nombre"] == "NOMBRE":
                record.nombre = atributo.string
            if atributo.attrs["nombre"] == "DESCRIPCION-ENTIDAD":
                record.descripcion = atributo.string
            if atributo.attrs["nombre"] == "ACCESIBILIDAD":
                record.accesibilidad = atributo.string
            if atributo.attrs["nombre"] == "CONTENT-URL":
                record.url = atributo.string
            if atributo.attrs["nombre"] == "LOCALIDAD":
                record.localidad = atributo.string
            if atributo.attrs["nombre"] == "NOMBRE-VIA":
                record.nombre_via = atributo.string.replace("&", "&amp")
            if atributo.attrs["nombre"] == "CLASE-VIAL":
                record.clase_vial = atributo.string
            if atributo.attrs["nombre"] == "PROVINCIA":
                record.provincia = atributo.string
            if atributo.attrs["nombre"] == "CODIGO-POSTAL":
                record.codigo_postal = atributo.string
            if atributo.attrs["nombre"] == "BARRIO":
                record.barrio = atributo.string
            if atributo.attrs["nombre"] == "DISTRITO":
                record.distrito = atributo.string
            if atributo.attrs["nombre"] == "COORDENADA-X":
                record.coord_x = atributo.string
            if atributo.attrs["nombre"] == "COORDENADA-Y":
                record.coord_y = atributo.string
            if atributo.attrs["nombre"] == "LATITUD":
                record.latitud = atributo.string
            if atributo.attrs["nombre"] == "LONGITUD":
                record.longitud = atributo.string
            if atributo.attrs["nombre"] == "TELEFONO":
                record.telefono = atributo.string
            if atributo.attrs["nombre"] == "EMAIL":
                record.email = atributo.string
        record.save()

