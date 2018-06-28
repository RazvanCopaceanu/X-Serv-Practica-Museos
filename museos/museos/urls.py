"""museos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from gestion import views
from django.contrib.auth.views import login, logout
from django.views.static import serve
from museos import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'static/terrafirma/default\.css$', views.css),
    url(r'static/(?P<path>.*)$', serve, {'document_root':
        '/home/razvan/SAT/X-Serv-Practica-Museos/museos/templates/'}),
    url(r'^about$', views.about, name="Información"),
    url(r'^$', views.main, name="Pagina principal"),
    url(r'^xml$', views.xmlmain, name="XML de la página principal"),
    url(r'^json$', views.json, name="JSON de la página principal"),
    url(r'^rss$', views.rss, name="RSS de los comentarios"),
    url(r'^museos$', views.museums, name="Página con todos los museos"),
    url(r'^museos/(\d+)$', views.museum, name="Página de un museo"),
    url(r'^registro$', views.registro),
    url(r'^logout$', views.logout_view),
    url(r'^login$', views.login_view),
    url(r'^(.+)/xml', views.xml, name="XML de la página de usuario"),
    url(r'^(.+)/json', views.jsonusuario, name="JSON de la página de usuario"),
    url(r'^(.+)', views.user, name="Pagina personal del usuario"),
]
