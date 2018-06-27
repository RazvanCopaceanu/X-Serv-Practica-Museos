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
