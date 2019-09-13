from django.db.models.functions import Concat
from django.db.models import Sum, Count, Q, Value, CharField, F
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from monitoring.common import get_localized_name as __

from .models import *
from .common import  dictfetchall

@csrf_exempt
@login_required
def proyecto(request):
    id = request.POST.get('proyecto')
    if id:
        proyecto = Project.objects.values().get(id=id)
        data = {'proyecto' : proyecto}
    else:
        data = {'proyecto' : None }
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
    parameters = {'proyecto': 'event__structure__project_id', 'desde': 'event__start__gte','hasta': 'event__start__lte'}
    filter_kwargs = filterBy(parameters, request)

    query = Attendance.objects
    if len(filter_kwargs)>0:
        query = query.filter(**filter_kwargs)

    result = query.order_by('event__structure_id', 'event__structure__description', 'event__structure__project__name').values(
        'event__structure_id', 'event__structure__description', 'event__structure__project__name').annotate(
        m=Count('id', filter=Q(contact__sex='M')),
        f=Count('id', filter=Q(contact__sex='F')),
        total=Count('id'))

    for row in result:
        row['name'] = str(row['event__structure__description']) + ' / ' + str(row['event__structure__project__name'])
        row['activity_id'] = row['event__structure_id']
    data = {'actividades': list(result) }
    return JsonResponse(data)


@csrf_exempt
@login_required
def paises(request):

    paises_todos = request.POST.get('paises_todos') == 'true'
    ninguno = False if request.POST.getlist("paises[]") or paises_todos else True
    parameters = {'paises[]': 'country__in','proyecto': 'structure__project','desde':'start__gte','hasta':'start__lte'}
    filter_kwargs = filterBy(parameters, request)
    filter_kwargs['id__isnull'] = False

    # TODO: check if this is really not needed here
    #result = Event.objects.filter(**filter_kwargs).order_by('country_id').distinct().values('country_id')
    result = Event.objects.all().order_by('country_id').distinct().values('country_id')

    for row in result:
        row['id'] =  row['country_id']
        row['country'] = row['country_id']
        row['active'] = True if row['country_id'] in request.POST.getlist("paises[]") or paises_todos else False
    data = {'paises': list(result), 'todos': paises_todos,  'ninguno': ninguno, }


    return JsonResponse(data)

@csrf_exempt
@login_required
def rubros(request):

    rubros_todos = request.POST.get('rubros_todos') == 'true'
    ninguno = False if request.POST.getlist("rubros[]") or rubros_todos else True
    proyecto_id = request.POST.get('proyecto')
    filter_kwargs = {'product__isnull':False}

    if(proyecto_id):
        filter_kwargs['project_id']=proyecto_id
    result = ProjectContact.objects.filter(**filter_kwargs).order_by(__('product__name')).distinct().values('product_id',__('product__name'))

    for row in result:
        row['rubro'] = row[__('product__name')]
        row['id'] = row['product_id']
        row['active'] = True if str(row['product_id']) in request.POST.getlist("rubros[]") or rubros_todos else False
    data = {'rubros': list(result), 'todos': rubros_todos,  'ninguno': ninguno, }

    return JsonResponse(data)


@csrf_exempt
@login_required
def graficoOrganizaciones(request):
    parameters = {'proyecto': 'structure__project_id', 'desde': 'start__gte','hasta': 'start__lte'}
    filter_kwargs = filterBy(parameters, request)

    query = Event.objects
    if len(filter_kwargs) > 0:
        query = query.filter(**filter_kwargs)

    organizaciones = query.order_by('organization_id', 'organization__name', 'organization__organization_type_id'). \
        values('organization_id', 'organization__name', 'organization__organization_type_id').distinct()

    org_list = []

    for row in organizaciones:
        org_list.append({'id': row['organization_id'], 'name': row['organization__name'], 'parent': row['organization__organization_type_id']})

    types = Event.objects.filter(**filter_kwargs).values('organization__organization_type_id', __('organization__organization_type__name'))

    colorNumero = 0
    colores = ['#B2BB1E', '#00AAA7', '#472A2B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655', '#FFF263', '#6AF9C4']
    data_dict = {}
    for v in types:
        v['color'] = colores[colorNumero % len(colores)]
        colorNumero += 1
        v['value'] = 0
        v['name'] = v[__('organization__organization_type__name')]
        data_dict[v['organization__organization_type_id']] = v
    for v in organizaciones:
        data_dict[v['organization__organization_type_id']]['value'] += 1

    result = list(data_dict.values()) + org_list
    data = {"organizaciones" : {"data" : result, "total" : len(organizaciones), "tipos" : data_dict, 'total_categorias' : len(data_dict) }}
    return JsonResponse(data)


@csrf_exempt
@login_required
def proyectosMetas(request):
    proyecto_id = request.POST.get('proyecto')
    if not proyecto_id:
        return JsonResponse({'proyectos_metas': []})
    proyecto = Project.objects.filter(id=proyecto_id).values('id', 'name', 'targetmen', 'targetwomen').first()
    result = []
    categorias = []
    serieMetaH = {'name' : 'Meta Hombres', 'color' : 'rgba(42,123,153,.9)', 'data' : [], 'pointPadding' : 0.3, 'pointPlacement' : -0.2}
    serieMetaF = {'name' : 'Meta Mujeres', 'color' : 'rgba(68,87,113,1)', 'data' : [], 'pointPadding' : 0.3, 'pointPlacement' : 0.2}
    serieH = {'name' : 'Cantidad Hombres', 'color' : 'rgba(255,205,85,.8)', 'data' : [], 'pointPadding' : 0.4, 'pointPlacement' : -0.2}
    serieF = {'name' : 'Cantidad Mujeres', 'color' : 'rgba(252,110,81,.8)', 'data' : [], 'pointPadding' : 0.4, 'pointPlacement' : 0.2}
    cursor = connection.cursor()
    categorias.append(proyecto['name'])
    serieMetaF['data'].append(proyecto['targetwomen'])
    serieMetaH['data'].append(proyecto['targetmen'])
    cursor.execute("SELECT COUNT(case when sex = 'F' then 1 else NULL end) AS f, COUNT(case when sex = 'M' then 1 else NULL end) AS m, count(sex) as total FROM (SELECT sex FROM (SELECT c.id, min(e.start) as start, c.sex, c.birthdate, education_id FROM attendance a LEFT JOIN contact c ON a.contact_id = c.id LEFT JOIN event e ON a.event_id = e.id LEFT JOIN country pa ON e.country_id= pa.id LEFT JOIN structure act ON e.structure_id = act.id LEFT JOIN project p ON act.project_id = p.id LEFT JOIN (SELECT p.id AS project_id, mp.id AS product_id FROM project p LEFT JOIN project_contact pc ON pc.project_id = p.id LEFT JOIN monitoring_product mp ON pc.product_id = mp.id GROUP BY p.id, mp.id) pc ON pc.project_id = p.id WHERE p.id='%s' GROUP BY c.id) sq) q" % (proyecto['id'],))
    query_result = dictfetchall(cursor)
    proyecto['meta_total'] = proyecto['targetmen'] + proyecto['targetwomen']
    totales = query_result[0]
    serieF['data'].append(totales['f'])
    serieH['data'].append(totales['m'])
    result.append(proyecto)
    result.append(totales)
    series = [serieMetaH, serieH, serieMetaF, serieF]
    agg_result = {'categorias' : categorias, 'series' : series, 'data' : result}
    return JsonResponse({'proyectos_metas': agg_result})

@csrf_exempt
@login_required
def graficoAnioFiscal(request):
    filter = getFilters(request)

    cursor = connection.cursor()
    cursor.execute("SELECT type, COUNT(case when sex = 'F' then 1 else NULL end) AS f, COUNT(case when sex = 'M' then 1 else NULL end) AS m, count(sex) as total FROM (SELECT id, CASE WHEN 10<=6 THEN CASE WHEN 10<= date_part( 'month', start) THEN  date_part( 'year',start)    ELSE  date_part( 'year',start)-1    END ELSE CASE WHEN 10 > date_part( 'month', start) THEN  date_part( 'year',start)    ELSE  date_part( 'year',start)+1    END END  as type, sex FROM (SELECT c.id, min(e.start) as start, c.sex, c.birthdate, education_id FROM attendance a LEFT JOIN contact c ON a.contact_id = c.id LEFT JOIN event e ON a.event_id = e.id LEFT JOIN country pa ON e.country_id= pa.id LEFT JOIN structure act ON e.structure_id = act.id LEFT JOIN project p ON act.project_id = p.id LEFT JOIN (SELECT p.id AS project_id, mp.name AS product FROM project p LEFT JOIN project_contact pc ON pc.project_id = p.id LEFT JOIN monitoring_product mp ON pc.product_id = mp.id GROUP BY p.id, mp.name) pc ON pc.project_id = p.id "+filter+" GROUP BY c.id) sq) q GROUP BY type ORDER BY type")
    result = dictfetchall(cursor)
    return JsonResponse({'fiscal': result})


@csrf_exempt
@login_required
def graficoEdad(request):

    filter = getFilters(request)
    cursor = connection.cursor()
    query = "SELECT filter.name AS type,\
                        COUNT(case when c.sex = 'F' then 1 else NULL end) AS f,\
                        COUNT(case when c.sex = 'M' then 1 else NULL end) AS m,\
                        COUNT(c.sex) as total\
                        FROM attendance a \
                        LEFT JOIN contact c ON a.contact_id = c.id \
                        LEFT JOIN event e ON a.event_id = e.id \
                   LEFT JOIN structure act ON e.structure_id = act.id \
                   LEFT JOIN project p ON act.project_id = p.id \
                        LEFT JOIN filter ON filter.slug='age' AND date_part('YEAR', age(birthdate)) \
                        BETWEEN CAST( filter.start as INTEGER) AND CAST( filter.end as INTEGER) "+filter+'  GROUP BY filter.name'

    cursor.execute(query)
    result = dictfetchall(cursor)
    return JsonResponse({'edad': result})


@csrf_exempt
@login_required
def graficoEducacion(request):
    parameters = {'proyecto': 'event__structure__project_id', 'desde': 'event__start__gte','hasta': 'event__start__lte'}
    filter_kwargs = filterBy(parameters, request)

    query = Attendance.objects
    if len(filter_kwargs)>0:
        query = query.filter(**filter_kwargs)

    result = query.order_by(__('contact__education__name')).values(__('contact__education__name')).annotate(
        m=Count('id', filter=Q(contact__sex='M')),
        f=Count('id', filter=Q(contact__sex='F')),
        total=Count('id'))
    for row in result:
        row['type'] = str(row[__('contact__education__name')])
    data = {'educacion': list(result) }
    return JsonResponse(data)


@csrf_exempt
@login_required
def graficoEventos(request):
    return JsonResponse({'foo':'bar'})


@csrf_exempt
@login_required
def graficoTipoParticipante(request):
    parameters = {'proyecto': 'event__structure__project_id', 'desde': 'event__start__gte', 'hasta': 'event__start__lte'}
    filter_kwargs = filterBy(parameters, request)

    query = Attendance.objects
    if len(filter_kwargs)>0:
        query = query.filter(**filter_kwargs)

    result = query.order_by(__('contact__type__name')).values(__('contact__type__name')).annotate(
        total=Count ('contact_id', distinct=True), f=Count('contact_id', distinct=True, filter=Q(contact__sex='F')), m=Count('contact_id', distinct=True, filter=Q(contact__sex='M'))
    )

    for row in result:
        row['type'] = row[__('contact__type__name')]
    data = list(result)
    return JsonResponse(data, safe=False)

@csrf_exempt
@login_required
def graficoSexoParticipante(request):
    parameters = {'proyecto': 'event__structure__project_id', 'desde': 'event__start__gte', 'hasta': 'event__start__lte'}
    filter_kwargs = filterBy(parameters, request)

    query = Attendance.objects
    if len(filter_kwargs)>0:
        query = query.filter(**filter_kwargs)

    result = query.aggregate(
        total=Count('contact_id', distinct=True), f=Count('contact_id', distinct=True, filter=Q(contact__sex='F')), m=Count('contact_id', distinct=True, filter=Q(contact__sex='M'))
    )
    return JsonResponse(result)

@csrf_exempt
@login_required
def graficoNacionalidad(request):
    filter = getFilters(request)
    cursor = connection.cursor()
    cursor.execute("SELECT name, count(sex) as total, COUNT(case when sex = 'F' then 1 else NULL end) AS f, COUNT(case when sex = 'M' then 1 else NULL end) AS m, name_es, x, y, country FROM (SELECT COALESCE(ca.name_es,'N/E') as country, ca.*, c.sex FROM attendance a LEFT JOIN contact c ON a.contact_id = c.id LEFT JOIN event e ON a.event_id = e.id LEFT JOIN country pa ON e.country_id= pa.id LEFT JOIN structure act ON e.structure_id = act.id LEFT JOIN project p ON act.project_id = p.id LEFT JOIN (SELECT p.id AS project_id, mp.name AS product FROM project p LEFT JOIN project_contact pc ON pc.project_id = p.id LEFT JOIN monitoring_product mp ON pc.product_id = mp.id GROUP BY p.id, mp.name) pc ON pc.project_id = p.id LEFT JOIN country ca ON c.country_id = ca.id "+filter+" GROUP BY c.id, ca.id) q GROUP BY country, name_es, name, x, y ORDER BY country")
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
    filter = getFilters(request)

    cursor = connection.cursor()
    cursor.execute("SELECT name, COUNT(sex) as total, COUNT(case when sex = 'F' then 1 else NULL end) AS f, COUNT(case when sex = 'M' then 1 else NULL end) AS m, name_es, x, y, id, count(distinct(eventos)) as eventos FROM (SELECT COALESCE(ca.name_es,'N/E') as country, ca.*, e.id AS eventos, c.sex FROM attendance a LEFT JOIN contact c ON a.contact_id = c.id LEFT JOIN event e ON a.event_id = e.id LEFT JOIN country pa ON e.country_id= pa.id LEFT JOIN structure act ON e.structure_id = act.id LEFT JOIN project p ON act.project_id = p.id LEFT JOIN (SELECT p.id AS project_id, mp.name AS product FROM project p LEFT JOIN project_contact pc ON pc.project_id = p.id LEFT JOIN monitoring_product mp ON pc.product_id = mp.id GROUP BY p.id, mp.name) pc ON pc.project_id = p.id LEFT JOIN country ca ON pa.id = ca.id "+filter+"  GROUP BY c.id, e.id, ca.id) q GROUP BY name, name_es, x, y, id ORDER BY name")
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

def filterBy(parameters, request):
    paises = request.POST.getlist("paises[]")
    filter_kwargs = {}

    for key, value in request.POST.items():
        if key in parameters:
            filter_kwargs[parameters[key]] = value if key!='paises[]' else paises

    return filter_kwargs

def getFilters(request):
    filter = ''
    if request.POST.get('proyecto') and request.POST.get('desde'):
        filter = " WHERE e.start>='" + request.POST.get('desde') + "' and e.start<='" + request.POST.get(
            'hasta') + "' and p.id=" + request.POST.get('proyecto')

    elif request.POST.get('proyecto'):
        filter = " WHERE p.id=" + request.POST.get('proyecto')
    elif request.POST.get('desde'):
        filter = " WHERE e.start>='" + request.POST.get('desde') + "' and e.start<='" + request.POST.get('hasta')

    return filter

