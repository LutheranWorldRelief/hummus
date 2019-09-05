from django.db.models.functions import Concat
from django.db.models import Sum, Count, Q, Value, CharField, F
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from django.utils import translation

@csrf_exempt
@login_required
def proyecto(request):
    data = {'proyecto': None}
    return JsonResponse(data)


@csrf_exempt
@login_required
def cantidadProyectos(request):
    proyectos = Project.objects.count()
    data = {'proyectos': proyectos }
    return JsonResponse(data)


@csrf_exempt
@login_required
def cantidadEventos(request):
    eventos = Event.objects.count()
    actividades = Event.objects.order_by('structure_id').distinct('structure_id').count()
    data = {"cantidadEventos": {"eventos": eventos ,"actividades": actividades} }
    return JsonResponse(data)


@csrf_exempt
@login_required
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
@login_required
def paises(request):
    result = Event.objects.order_by('country_id').values('country_id').distinct()
    for row in result:
        row['id'] =  row['country_id']
        row['country'] = row['country_id']
        row['active'] = row['id'] in request.POST.getlist("paises[]")
    data = {'paises': list(result), 'todos': False,  'ninguno': False, }

    return JsonResponse(data)


@csrf_exempt
@login_required
def rubros(request):
    result = Product.objects.all().values()
    for row in result:
        row['rubro'] = row['name_es']
        row['active'] = str(row['id']) in request.POST.getlist("rubros[]")
    data = {'rubros': list(result) }
    return JsonResponse(data)


@csrf_exempt
@login_required
def graficoOrganizaciones(request):
    organizaciones = Event.objects.order_by('organization_id', 'organization__name', 'organization__organization_type_id'). \
        values('organization_id', 'organization__name', 'organization__organization_type_id').distinct()
    org_list = []
    OrganizationType_column = get_select_column('name')

    for row in organizaciones:
        org_list.append({'id': row['organization_id'], 'name': row['organization__name'], 'parent': row['organization__organization_type_id']})
    types = OrganizationType.objects.values('id', OrganizationType_column)
    colorNumero = 0;
    colores = ['#B2BB1E', '#00AAA7', '#472A2B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4'];
    data_dict = {}
    for v in types:
        v['color'] = colores[colorNumero % 10]
        colorNumero += 1
        v['value'] = 0
        data_dict[v['id']] = v
    for v in organizaciones:
        data_dict[v['organization__organization_type_id']]['value'] += 1;

    result = list(data_dict.values()) + org_list
    data = {"organizaciones" : {"data" : result, "total" : len(organizaciones), "tipos" : data_dict, 'total_categorias' : len(data_dict) }}
    return JsonResponse(data)


@csrf_exempt
@login_required
def proyectosMetas(request):
    return JsonResponse({'proyectos_metas': []})


@csrf_exempt
@login_required
def graficoAnioFiscal(request):
    cursor = connection.cursor()
    cursor.execute("SELECT type, COUNT(case when sex = 'F' then 1 else NULL end) AS f, COUNT(case when sex = 'M' then 1 else NULL end) AS m, count(sex) as total FROM (SELECT id, CASE WHEN 10<=6 THEN CASE WHEN 10<= date_part( 'month', start) THEN  date_part( 'year',start)    ELSE  date_part( 'year',start)-1    END ELSE CASE WHEN 10 > date_part( 'month', start) THEN  date_part( 'year',start)    ELSE  date_part( 'year',start)+1    END END  as type, sex FROM (SELECT c.id, min(e.start) as start, c.sex, c.birthdate, education_id FROM attendance a LEFT JOIN contact c ON a.contact_id = c.id LEFT JOIN event e ON a.event_id = e.id LEFT JOIN country pa ON e.country_id= pa.id LEFT JOIN structure act ON e.structure_id = act.id LEFT JOIN project p ON act.project_id = p.id LEFT JOIN (SELECT p.id AS project_id, mp.name AS product FROM project p LEFT JOIN project_contact pc ON pc.project_id = p.id LEFT JOIN monitoring_product mp ON pc.product_id = mp.id GROUP BY p.id, mp.name) pc ON pc.project_id = p.id GROUP BY c.id) sq) q GROUP BY type ORDER BY type")
    result = dictfetchall(cursor)
    return JsonResponse({'fiscal': result})


@csrf_exempt
@login_required
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
@login_required
def graficoEducacion(request):
    education_column = get_select_column('education__name')

    result = Contact.objects.order_by(education_column).values(education_column).annotate(
        m=Count('id', filter=Q(sex='M')),
        f=Count('id', filter=Q(sex='M')),
        total=Count('id'))
    for row in result:
        row['type'] = str(row[education_column])
    data = {'educacion': list(result) }
    return JsonResponse(data)


@csrf_exempt
@login_required
def graficoEventos(request):
    return JsonResponse({'foo':'bar'})


@csrf_exempt
@login_required
def graficoTipoParticipante(request):
    contacttype_column=get_select_column('contact__type__name')

    result = Attendance.objects.order_by(contacttype_column).values(contacttype_column).annotate(
        total=Count('contact_id', distinct=True), f=Count('contact_id', distinct=True, filter=Q(contact__sex='F')), m=Count('contact_id', distinct=True, filter=Q(contact__sex='M'))
    )
    for row in result:
        row['type'] = row[contacttype_column]
    data = list(result)
    return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def graficoSexoParticipante(request):
    result = Attendance.objects.aggregate(
        total=Count('contact_id', distinct=True), f=Count('contact_id', distinct=True, filter=Q(contact__sex='F')), m=Count('contact_id', distinct=True, filter=Q(contact__sex='M'))
    )
    return JsonResponse(result)


@csrf_exempt
@login_required
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
@login_required
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

def get_select_column(column):
    language_user = translation.get_language()
    if (language_user != 'en'):
        column += '_' + language_user
    return column
