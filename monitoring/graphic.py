from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *

@csrf_exempt
def proyecto(request):
    data = {'proyecto': None}
    return JsonResponse(data)

@csrf_exempt
def cantidadProyectos(request):
    proyectos = Project.objects.count()
    data = {'proyectos': proyectos }
    return JsonResponse(data)

@csrf_exempt
def cantidadEventos(request):
    eventos = Event.objects.count()
    actividades = Event.objects.order_by('structure_id').distinct('structure_id').count()
    data = {"cantidadEventos": {"eventos": eventos ,"actividades": actividades} }
    return JsonResponse(data)

@csrf_exempt
def graficoActividades(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def paises(request):
    paises = Country.objects.count()
    data = {'paises': paises }
    return JsonResponse(data)

@csrf_exempt
def rubros(request):
    rubros = Product.objects.count()
    data = {'rubros': rubros }
    return JsonResponse(data)

@csrf_exempt
def graficoOrganizaciones(request):
    organizaciones = Organization.objects.values('name', 'organization_type_id')
    types = OrganizationType.objects.values('id', 'name')
    colorNumero = 0;
    colores = ['#B2BB1E', '#00AAA7', '#472A2B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'];
    data_array = {}
    for v in types:
        v['color'] = colores[colorNumero % 10]
        colorNumero += 1
        v['value'] = 0
        data_array[v['id']] = v
    for v in organizaciones:
        data_array[v['organization_type_id']]['value'] += 1;

    data = {"organizaciones" : {"data" : data_array }}
    return JsonResponse(data)

@csrf_exempt
def proyectosMetas(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoAnioFiscal(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoEdad(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoEducacion(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoEventos(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoTipoParticipante(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoSexoParticipante(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoNacionalidad(request):
    return JsonResponse({'foo':'bar'})

@csrf_exempt
def graficoPaisEventos(request):
    return JsonResponse({'foo':'bar'})
