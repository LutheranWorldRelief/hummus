from django.shortcuts import render
from django.views.generic import TemplateView
from django_tables2 import RequestConfig

from .tables import *
from .models import *


class ProjectTableView(PagedFilteredTableView):
    model = Project
    table_class = ProjectTable
    template_name = 'contact_table.html'
    paginate_by = 50
    filter_class = ProjectFilter
    formhelper_class = ProjectFilterFormHelper


class ContactTableView(PagedFilteredTableView):
    model = Contact
    table_class = ContactTable
    template_name = 'contact_table.html'
    paginate_by = 50
    filter_class = ContactFilter
    formhelper_class = ContactFilterFormHelper


class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    pass


def proyecto(request):
    pass

def cantidadProyectos(request):
    pass

def cantidadEventos(request):
    pass

def graficoActividades(request):
    pass

def paises(request):
    pass

def rubros(request):
    pass

def graficoOrganizaciones(request):
    pass

def proyectosMetas(request):
    pass

def graficoAnioFiscal(request):
    pass

def graficoEdad(request):
    pass

def graficoEducacion(request):
    pass

def graficoEventos(request):
    pass

def graficoTipoParticipante(request):
    pass

def graficoSexoParticipante(request):
    pass

def graficoNacionalidad(request):
    pass

def graficoPaisEventos(request):
    pass
