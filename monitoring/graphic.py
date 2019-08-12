from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Concat
from django.db.models import Sum, Count, Q, Value, CharField
from django.db import connection

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
    result = Attendance.objects.order_by('event__structure_id', 'event__structure__description', 'event__structure__project__name').values(
        'event__structure_id', 'event__structure__description', 'event__structure__project__name').annotate(
        m=Count('id', filter=Q(sex='M')),
        f=Count('id', filter=Q(sex='M')),
        total=Count('id'))
    for row in result:
        row['name'] = str(row['event__structure__description']) + ' / ' + str(row['event__structure__project__name'])
        row['activity_id'] = row['event__structure_id']
    data = {'actividades': list(result) }
    return JsonResponse(data)

@csrf_exempt
def paises(request):
    paises = Country.objects.count()
    data = {'paises': paises }
    return JsonResponse(data)

@csrf_exempt
def rubros(request):
    result = Product.objects.all().values()
    for row in result:
        row['rubro'] = row['name_es']
    data = {'rubros': list(result) }
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

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
@csrf_exempt
def graficoEdad(request):
    cursor = connection.cursor()
    cursor.execute("SELECT filter.name AS type, \
                        COUNT(case when sex = 'F' then 1 else NULL end) AS f, \
                        COUNT(case when sex = 'M' then 1 else NULL end) AS m, \
                        COUNT(sex) as total \
                        FROM contact \
			JOIN filter ON filter.slug='age' AND date_part('YEAR', age(birthdate)) \
			BETWEEN CAST( filter.start as INTEGER) AND CAST( filter.end as INTEGER) \
                        GROUP BY filter.name ")
    result = dictfetchall(cursor)
    return JsonResponse({'edad': result})

@csrf_exempt
def graficoEducacion(request):
    result = Contact.objects.order_by('education__name').values('education__name').annotate(
        m=Count('id', filter=Q(sex='M')),
        f=Count('id', filter=Q(sex='M')),
        total=Count('id'))
    for row in result:
        row['type'] = str(row['education__name'])
    data = {'educacion': list(result) }
    return JsonResponse(data)

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
