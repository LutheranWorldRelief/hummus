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
    result = Event.objects.order_by('country_id').values('country_id').distinct()
    for row in result:
        row['id'] =  row['country_id']
        row['country'] = row['country_id']
    data = {'paises': list(result) }
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
    cursor = connection.cursor()
    cursor.execute("SELECT type, COUNT(case when sex = 'F' then 1 else NULL end) AS f, COUNT(case when sex = 'M' then 1 else NULL end) AS m, count(sex) as total FROM (SELECT id, CASE WHEN 10<=6 THEN CASE WHEN 10<= date_part( 'month', start) THEN  date_part( 'year',start)    ELSE  date_part( 'year',start)-1    END ELSE CASE WHEN 10 > date_part( 'month', start) THEN  date_part( 'year',start)    ELSE  date_part( 'year',start)+1    END END  as type, sex FROM (SELECT c.id, min(e.start) as start, c.sex, c.birthdate, education_id FROM attendance a LEFT JOIN contact c ON a.contact_id = c.id LEFT JOIN event e ON a.event_id = e.id LEFT JOIN country pa ON e.country_id= pa.id LEFT JOIN structure act ON e.structure_id = act.id LEFT JOIN project p ON act.project_id = p.id LEFT JOIN (SELECT p.id AS project_id, mp.name AS product FROM project p LEFT JOIN project_contact pc ON pc.project_id = p.id LEFT JOIN monitoring_product mp ON pc.product_id = mp.id GROUP BY p.id, mp.name) pc ON pc.project_id = p.id GROUP BY c.id) sq) q GROUP BY type ORDER BY type")
    result = dictfetchall(cursor)
    return JsonResponse({'fiscal': result})


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
    result = Attendance.objects.aggregate(
        total=Count('contact_id', distinct=True), f=Count('contact_id', distinct=True, filter=Q(contact__sex='F')), m=Count('contact_id', distinct=True, filter=Q(contact__sex='M'))
    )
    return JsonResponse(result)

@csrf_exempt
def graficoNacionalidad(request):
    cursor = connection.cursor()
    cursor.execute("SELECT name, count(sex) as total, COUNT(case when sex = 'F' then 1 else NULL end) AS f, COUNT(case when sex = 'M' then 1 else NULL end) AS m, name_es, x, y, country FROM (SELECT COALESCE(ca.name_es,'N/E') as country, ca.*, c.sex FROM attendance a LEFT JOIN contact c ON a.contact_id = c.id LEFT JOIN event e ON a.event_id = e.id LEFT JOIN country pa ON e.country_id= pa.id LEFT JOIN structure act ON e.structure_id = act.id LEFT JOIN project p ON act.project_id = p.id LEFT JOIN (SELECT p.id AS project_id, mp.name AS product FROM project p LEFT JOIN project_contact pc ON pc.project_id = p.id LEFT JOIN monitoring_product mp ON pc.product_id = mp.id GROUP BY p.id, mp.name) pc ON pc.project_id = p.id LEFT JOIN country ca ON c.country_id = ca.id GROUP BY c.id, ca.id) q GROUP BY country, name_es, name, x, y ORDER BY country")
    result = dictfetchall(cursor)
    pais_array = [];
    for row in result:
        if 'country' in row:
            pais_array.append([
                row['name'],
                row['total'],
                row['f'],
                row['m'],
                row['x'],
                row['y'],
                row['name_es'],
                str(row['country']).lower(),
            ])

    return JsonResponse({'pais': result, 'paisArray': pais_array})

@csrf_exempt
def graficoPaisEventos(request):
    cursor = connection.cursor()
    cursor.execute("SELECT name, COUNT(sex) as total, COUNT(case when sex = 'F' then 1 else NULL end) AS f, COUNT(case when sex = 'M' then 1 else NULL end) AS m, name_es, x, y, id, count(distinct(eventos)) as eventos FROM (SELECT COALESCE(ca.name_es,'N/E') as country, ca.*, e.id AS eventos, c.sex FROM attendance a LEFT JOIN contact c ON a.contact_id = c.id LEFT JOIN event e ON a.event_id = e.id LEFT JOIN country pa ON e.country_id= pa.id LEFT JOIN structure act ON e.structure_id = act.id LEFT JOIN project p ON act.project_id = p.id LEFT JOIN (SELECT p.id AS project_id, mp.name AS product FROM project p LEFT JOIN project_contact pc ON pc.project_id = p.id LEFT JOIN monitoring_product mp ON pc.product_id = mp.id GROUP BY p.id, mp.name) pc ON pc.project_id = p.id LEFT JOIN country ca ON pa.id = ca.id GROUP BY c.id, e.id, ca.id) q GROUP BY name, name_es, x, y, id ORDER BY name")
    result = dictfetchall(cursor)
    pais_array = [];
    for row in result:
        if 'id' in row:
            pais_array.append([
                row['name'],
                row['total'],
                row['f'],
                row['m'],
                row['x'],
                row['y'],
                row['name_es'],
                str(row['id']).lower(),
                row['eventos']
            ])

    return JsonResponse({'pais': result, 'paisArray': pais_array})
