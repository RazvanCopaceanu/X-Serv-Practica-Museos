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


@csrf_exempt
def main(request):
    template = get_template("terrafirma/index.html")
    museos = ""
    lista_museos = Museos.objects.all()
    if len(lista_museos) == 0:
        if request.method == 'GET':
            boton = "<form method = 'POST'><button type='submit' "
            boton += "name='Cargar' value=1>Cargar información de "
            boton += "museos</button><br>"
            c = RequestContext(request, {'boton': boton})
        elif request.method == 'POST':
            datos = request.body.decode('utf-8').split("=")[1]
            parser()
            return HttpResponseRedirect('/')
        else:
            template = get_template("terrafirma/error.html")
            c = RequestContext(request, {'error': "Method not allowed"})
            response = template.render(c)
            return HttpResponse(response, status=405)
    else:
        if request.method == 'GET':
            lista_museos = Museo.objects.all().order_by('-n_coment')
            lista_museos = lista_museos.exclude(n_coment=0)
            lista_museos = lista_museos[0:5]
            boton = "<form method = 'POST'><button type='submit' "
            boton += "name='Accesibilidad' value=1>"
            boton += "Mostrar museos accesibles</button>"
        elif request.method == 'POST':
            accesibilidad = request.body.decode('utf-8').split("=")[1]
            if int(accesibilidad) == 1:
                lista_museos = Museo.objects.all().order_by('-n_coment')
                lista_museos = lista_museos.exclude(n_coment=0)
                lista_museos = lista_museos.filter(accesibilidad=1)
                lista_museos = lista_museos[0:5]
                boton = "<form method = 'POST'><button type='submit' "
                boton += "name='Accesibilidad' value=0>Mostrar "
                boton += "todos los museos</button>"
            elif int(accesibilidad) == 0:
                lista_museos = Museo.objects.all().order_by('-n_coment')
                lista_museos = lista_museos.exclude(n_coment=0)
                lista_museos = lista_museos[0:5]
                boton = "<form method = 'POST'><button type='submit' "
                boton += "name='Accesibilidad' value=1>"
                boton += "Mostrar museos accesibles</button>"
        else:
            template = get_template("terrafirma/error.html")
            c = RequestContext(request, {'error': "Method not allowed"})
            response = template.render(c)
            return HttpResponse(response, status=405)
        lista_personales = ""
        lista_usuarios = User.objects.all()
        for user in lista_usuarios:
            try:
                titulo = PaginaUsuario.objects.get(usuario=user.id).titulo
                if titulo == "":
                    lista_personales += "<a href='/" + user.username + "'>Pagi"
                    lista_personales += "na de " + user.username + "</a><br>"
                else:
                    lista_personales += "<a href='/" + user.username + "'>"
                    lista_personales += titulo + "</a><br>"
            except PaginaUsuario.DoesNotExist:
                lista_personales += "<a href='/" + user.username + "'>Pagina "
                lista_personales += "de " + user.username + "</a><br>"
        c = RequestContext(request, {'Lateral': lista_personales, 'museos': lista_museos, 'boton': boton})
    response = template.render(c)
    return HttpResponse(response, status=200)


def formulariolista(request, resource):
    if str(request.user) == str(resource):
        formulario = "<form id='formTitulo' action='/" + str(resource)
        formulario += "' method='POST'>Introduce un nuevo titulo para "
        formulario += "tu lista personal: <br><input type='text' "
        formulario += "name='Titulo'><input type='submit'"
        formulario += " value='Enviar'></form>"
        formulario += "<form id='formTitulo' action='/" + str(resource)
        formulario += "' method='POST'>Introduce un nuevo color de fondo "
        formulario += "para tu lista personal: <br><input type='text' "
        formulario += "name='Color'><input type='submit'"
        formulario += " value='Enviar'></form>"
        formulario += "<form id='formTitulo' action='/" + str(resource)
        formulario += "' method='POST'>Introduce un nuevo tamaño de letra "
        formulario += "para tu lista personal: <br><input type='text' "
        formulario += "name='Size'><input type='submit'"
        formulario += " value='Enviar'></form>"
    else:
        formulario = ""
return (formulario)


def museoselegidos(request, resource):
    usuario = User.objects.get(username=resource)
    elegidos = Elegidos.objects.filter(usuario=usuario)
    opcion = request.body.decode('utf-8').split("=")[0]
    anterior = ""
    siguiente = ""
    if opcion == 'next':
        n = request.body.decode('utf-8').split("=")[1]
        m = int(n)+5
        anterior = "<form action='/" + resource + "' method='POST'><button"
        anterior += " type='submit' name='previous' value='" + n + "'"
        anterior += " class='btn-link'>Anterior</button></form>"
        if len(elegidos) >= m:
            siguiente = "<form action='/" + resource + "' method='POST'><button"
            siguiente += " type='submit' name='next' value='" + str(m) + "'"
            siguiente += " class='btn-link'>Siguiente</button></form>"
        else:
            siguiente = ""
        elegidos = elegidos[int(n):m]
    elif opcion == 'previous':
        m = request.body.decode('utf-8').split("=")[1]
        n = int(m)-5
        if n == 0:
            anterior = ""
        else:
            anterior = "<form action='/" + resource + "' method='POST'><button"
            anterior += " type='submit' name='previous' value='" + str(n) + "'"
            anterior += " class='btn-link'>Anterior</button></form>"
        siguiente = "<form action='/" + resource + "' method='POST'><button"
        siguiente += " type='submit' name='next' value='" + m + "'"
        siguiente += " class='btn-link'>Siguiente</button></form>"
        elegidos = elegidos[n:int(m)]
    else:
        if len(elegidos) > 5:
            elegidos = elegidos[0:5]
            anterior = ""
            siguiente = "<form action='/" + resource + "' method='POST'><button"
            siguiente += " type='submit' name='next' value='5'"
            siguiente += " class='btn-link'>Siguiente</button></form>"
    return(elegidos, siguiente, anterior)


@csrf_exempt
def user(request, resource):
    formulario = ""
    template = get_template("terrafirma/user.html")
    if request.method == 'GET':
        try:
            usuario = User.objects.get(username=resource)
            lista_personal = PaginaUsuario.objects.get(usuario=usuario)
            if lista_personal.titulo == "":
                titulo = "Página de " + usuario.username
            else:
                titulo = lista_personal.titulo
            formulario = formulariolista(request, resource)
        except User.DoesNotExist:
            template = get_template("terrafirma/error.html")
            c = RequestContext(request, {'error': "Usuario no existente"})
            response = template.render(c)
            return HttpResponse(response, status=404)
        except PaginaUsuario.DoesNotExist:
            pagina_personal = PaginaUsuario(usuario=usuario)
            pagina_personal.save()
            formulario = formulariolista(request, resource)
            response = "La lista esta vacia<br>" + formulario
            return HttpResponseRedirect('/' + resource)
    elif request.method == 'POST':
        opcion = request.body.decode('utf-8').split("=")[0]
        formulario = formulariolista(request, resource)
        if opcion == 'Titulo':
            if str(request.user) == str(resource):
                titulo = request.body.decode('utf-8').split("=")[1].replace("+", " ")
                usuario = User.objects.get(username=resource)
                pagina_personal = PaginaUsuario.objects.get(usuario=usuario)
                pagina_personal.titulo = titulo
                pagina_personal.save()
        elif opcion == 'Color':
            color = request.body.decode('utf-8').split("=")[1]
            usuario = User.objects.get(username=resource)
            pagina_personal = PaginaUsuario.objects.get(usuario=usuario)
            pagina_personal.color = color
            pagina_personal.save()
        elif opcion == 'Size':
            size = request.body.decode('utf-8').split("=")[1]
            usuario = User.objects.get(username=resource)
            pagina_personal = PaginaUsuario.objects.get(usuario=usuario)
            pagina_personal.size = size
            pagina_personal.save()
        elif opcion == 'next':
            (elegidos, siguiente, anterior) = museosselegidos(request, resource)
        elif opcion == 'previous':
            (elegidos, siguiente, anterior) = museoselegidos(request, resource)
    else:
        template = get_template("terrafirma/error.html")
        c = RequestContext(request, {'error': "Method not allowed"})
        response = template.render(c)
        return HttpResponse(response, status=405)
    (elegidos, siguiente, anterior) = museoselegidos(request, resource)
    c = RequestContext(request, {'elegidos': elegidos, 'formulario': formulario, 'siguiente': siguiente, 'anterior': anterior, 'usuario': resource})
    response = template.render(c)
    return HttpResponse(response, status=200)


@csrf_exempt
def museums(request):
    response = ""
    museums = ""
    if request.method == 'GET':
        lista_museos = Museo.objects.all()
        for a in lista_museos:
            museums += "<a href='/museos/" + str(a.id)
            museums += "'>" + a.nombre + "</a><br>"
        distritos = lista_museos.order_by().values_list('distrito', flat=True).distinct()
        formulario = "<form method='POST'>Filtrado por distrito: "
        formulario += "<select name='Distrito'>"
        for element in distritos:
            formulario += "<option value='" + element + "'>"
            formulario += element + "</option>"
        formulario += "</select><input type='submit' value='Enviar'></form>"
        response = formulario + museos
    elif request.method == 'POST':
        distrito = request.body.decode('utf-8').split("=")[1]
        lista_museos = Museo.objects.all().filter(distrito=distrito)
        museums += "Museos del distrito \"" + distrito + "\":<br>"
        for a in lista_museos:
            museums += "<a href='/museos/" + str(a.id)
            museums += "'>" + a.nombre + "</a><br>"
        distritos = Museo.objects.order_by().values_list('distrito', flat=True).distinct()
        formulario = "<form method='POST'>Filtrado por distrito: "
        formulario += "<select name='Distrito'>"
        for element in distritos:
            formulario += "<option value='" + element + "'>"
            formulario += element + "</option>"
        formulario += "</select><input type='submit' value='Enviar'></form>"
    else:
        template = get_template("terrafirma/error.html")
        c = RequestContext(request, {'error': "Method not allowed"})
        response = template.render(c)
        return HttpResponse(response, status=405)
    template = get_template("terrafirma/museos.html")
    c = RequestContext(request, {'Museums': formulario + museums})
    response = template.render(c)
return HttpResponse(response, status=200)

