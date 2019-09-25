from datetime import date

from django.utils.timezone import now
from django.db.models.functions import Concat
from django.db.models import Sum, Count, Q, Value, CharField, F
from django.db.models.functions import ExtractYear
from django.db.models import CharField, Case, Value, When
from django.db import connection
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .common import dictfetchall, get_localized_name as __


@csrf_exempt
@login_required
def proyecto(request):
    id = request.POST.get('proyecto')
    if id:
        proyecto = Project.objects.values().get(id=id)
        data = {'proyecto': proyecto}
    else:
        data = {'proyecto': None}
    return JsonResponse(data)


@csrf_exempt
@login_required
def cantidadProyectos(request):
    proyectos = Project.objects.count()
    data = {'proyectos': proyectos}
    return JsonResponse(data)


@csrf_exempt
@login_required
def cantidadEventos(request):
    return JsonResponse({})  # FIXME


@csrf_exempt
@login_required
def graficoActividades(request):
    return JsonResponse({})  # FIXME


@csrf_exempt
@login_required
def paises(request):
    paises_todos = request.POST.get('paises_todos') == 'true'
    ninguno = False if request.POST.getlist("paises[]") or paises_todos else True
    parameters = {'paises[]': 'country__in', 'proyecto': 'project', 'desde': 'start__gte', 'hasta': 'start__lte'}
    filter_kwargs = filterBy(parameters, request)
    filter_kwargs['id__isnull'] = False

    # TODO: check if this is really not needed here
    # result = Event.objects.filter(**filter_kwargs).order_by('country_id').distinct().values('country_id')
    result = Project.objects \
        .filter(countries__isnull=False) \
        .all() \
        .order_by('countries__id') \
        .values('countries__id', 'countries__name') \
        .distinct()

    for row in result:
        row['id'] = row['countries__id']
        row['country'] = row['countries__id']
        row['active'] = True if row['countries__id'] in request.POST.getlist("paises[]") or paises_todos else False
    data = {'paises': list(result), 'todos': paises_todos, 'ninguno': ninguno, }

    return JsonResponse(data)


@csrf_exempt
@login_required
def rubros(request):
    rubros_todos = request.POST.get('rubros_todos') == 'true'
    ninguno = False if request.POST.getlist("rubros[]") or rubros_todos else True
    proyecto_id = request.POST.get('proyecto')
    filter_kwargs = {'product__isnull': False}

    if (proyecto_id):
        filter_kwargs['project_id'] = proyecto_id
    result = ProjectContact.objects.filter(**filter_kwargs).order_by(__('product__name')).distinct().values(
        'product_id', __('product__name'))

    for row in result:
        row['rubro'] = row[__('product__name')]
        row['id'] = row['product_id']
        row['active'] = True if str(row['product_id']) in request.POST.getlist("rubros[]") or rubros_todos else False
    data = {'rubros': list(result), 'todos': rubros_todos, 'ninguno': ninguno, }

    return JsonResponse(data)


@csrf_exempt
@login_required
def graficoOrganizaciones(request):
    parameters = {'paises[]': 'contact__country__in', 'rubros[]': 'product__in',
                  'proyecto': 'project', 'desde': 'date_entry_project__gte', 'hasta': 'date_entry_project__lte'}
    filter_kwargs = filterBy(parameters, request)  # filterBy(parameters, request)

    organizaciones = ProjectContact.objects.filter(**filter_kwargs).order_by('organization_id'). \
        values('organization_id', 'organization__name', 'organization__organization_type_id').distinct()

    org_list = []

    for row in organizaciones:
        org_list.append({'id': row['organization_id'], 'name': row['organization__name'],
                         'parent': row['organization__organization_type_id']})

    types = ProjectContact.objects.filter(**filter_kwargs).order_by('organization__organization_type_id') \
        .values('organization__organization_type_id', __('organization__organization_type__name')).distinct()

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

    return JsonResponse({'organizaciones': {'data': result, 'total': len(organizaciones), 'tipos': data_dict,
                                            'total_categorias': len(data_dict)}})


@csrf_exempt
@login_required
def proyectosMetas(request):
    proyecto_id = request.POST.get('proyecto')
    if not proyecto_id:
        return JsonResponse({'proyectos_metas': []})
    proyecto = Project.objects.filter(id=proyecto_id).values('id', 'name', 'targetmen', 'targetwomen').first()
    result = []
    categorias = []
    serieMetaH = {'name': _('Goal Men'), 'color': 'rgba(42,123,153,.9)', 'data': [], 'pointPadding': 0.3,
                  'pointPlacement': -0.2}
    serieMetaF = {'name': _('Goal Women'), 'color': 'rgba(68,87,113,1)', 'data': [], 'pointPadding': 0.3,
                  'pointPlacement': 0.2}
    serieH = {'name': _('Amount Men'), 'color': 'rgba(255,205,85,.8)', 'data': [], 'pointPadding': 0.4,
              'pointPlacement': -0.2}

    serieF = {'name': _('Amount Women'), 'color': 'rgba(252,110,81,.8)', 'data': [], 'pointPadding': 0.4,
              'pointPlacement': 0.2}

    categorias.append(proyecto['name'])
    serieMetaF['data'].append(proyecto['targetwomen'])
    serieMetaH['data'].append(proyecto['targetmen'])
    totales = ProjectContact.objects.filter(project_id=proyecto['id']).aggregate(
        f=Count('contact', filter=Q(contact__sex='F')), m=Count('contact', filter=Q(contact__sex='M')))
    totales['total'] = totales['f'] + totales['m']
    if proyecto['targetmen'] and proyecto['targetwomen']:
        proyecto['meta_total'] = proyecto['targetmen'] + proyecto['targetwomen']
    else:
        proyecto['meta_total'] = None
    serieF['data'].append(totales['f'])
    serieH['data'].append(totales['m'])
    result.append(proyecto)
    result.append(totales)
    series = [serieMetaH, serieH, serieMetaF, serieF]
    agg_result = {'categorias': categorias, 'series': series, 'data': result}
    return JsonResponse({'proyectos_metas': agg_result})


@csrf_exempt
@login_required
def graficoAnioFiscal(request):
    parameters = {'proyecto': 'project__id', 'desde': 'date_entry_project__gte', 'hasta': 'date_entry_project__lte'}
    filter_kwargs = filterBy(parameters, request)
    result = ProjectContact.objects.filter(**filter_kwargs).values(type=ExtractYear('project__start')).order_by(
        'type').annotate(
        f=Count('contact', filter=Q(contact__sex='F')),
        m=Count('contact', filter=Q(contact__sex='M')),
        total=Count('contact__sex')
    )

    return JsonResponse({'fiscal': list(result)})


@csrf_exempt
@login_required
def graficoEdad(request):
    parameters = {'proyecto': 'project__id', 'desde': 'date_entry_project__gte', 'hasta': 'date_entry_project__lte'}
    filter_kwargs = filterBy(parameters, request)
    groups = Filter.objects.filter(slug='age', start__gte=0)
    named_groups = []
    for group in groups:
        current = now().date()
        min_date = date(current.year - group.end, current.month, current.day)
        max_date = date(current.year - group.start, current.month, current.day)
        filter_kwargs['contact__birthdate__gte'] = min_date
        filter_kwargs['contact__birthdate__lte'] = max_date
        row = ProjectContact.objects.filter(**filter_kwargs).aggregate(
            f=Count('contact', filter=Q(contact__sex='F')), m=Count('contact', filter=Q(contact__sex='M'))
        )
        row['total'] = row['f'] + row['m']
        row['type'] = group.name
        named_groups.append(row)

    result = named_groups
    return JsonResponse({'edad': result})


@csrf_exempt
@login_required
def graficoEducacion(request):
    parameters = {'proyecto': 'project_id', 'desde': 'projectcontact__start__gte',
                  'hasta': 'projectcontact__start__lte'}
    filter_kwargs = {}  # filterBy(parameters, request)

    query = ProjectContact.objects
    if len(filter_kwargs) > 0:
        query = query.filter(**filter_kwargs)

    result = query.order_by(__('contact__education__name')).values(__('contact__education__name')).annotate(
        m=Count('id', filter=Q(contact__sex='M')),
        f=Count('id', filter=Q(contact__sex='F')),
        total=Count('id'))
    for row in result:
        row['type'] = str(row[__('contact__education__name')])
    data = {'educacion': list(result)}
    return JsonResponse(data)


@csrf_exempt
@login_required
def graficoEventos(request):
    return JsonResponse({'foo': 'bar'})


@csrf_exempt
@login_required
def graficoTipoParticipante(request):
    parameters = {'proyecto': 'project__id', 'desde': 'date_entry_project__gte', 'hasta': 'date_entry_project__lte'}
    filter_kwargs = filterBy(parameters, request)
    result = ProjectContact.objects.filter(**filter_kwargs).order_by(__('contact__type__name')).values(
        __('contact__type__name')).annotate(
        type=Case(When(contact__type__name=None, then=Value('NE')), default=__('contact__type__name'),
                  output_field=CharField()),
        total=Count('contact_id', distinct=True), f=Count('contact_id', distinct=True, filter=Q(contact__sex='F')),
        m=Count('contact_id', distinct=True, filter=Q(contact__sex='M'))
    )

    for row in result:
        row['type'] = row['type']
    data = list(result)
    return JsonResponse(data, safe=False)


@csrf_exempt
@login_required
def graficoSexoParticipante(request):
    parameters = {'paises[]': 'contact__country__in', 'rubros[]': 'product__in',
                  'proyecto': 'project', 'desde': 'date_entry_project__gte', 'hasta': 'date_entry_project__lte'}
    filter_kwargs = filterBy(parameters, request)  # filterBy(parameters, request)

    result = ProjectContact.objects.filter(**filter_kwargs).aggregate(
        total=Count('contact_id', distinct=True), f=Count('contact_id', distinct=True, filter=Q(contact__sex='F')),
        m=Count('contact_id', distinct=True, filter=Q(contact__sex='M'))
    )
    return JsonResponse(result)


@csrf_exempt
@login_required
def graficoNacionalidad(request):
    parameters = {'paises[]': 'contact__country__in', 'rubros[]': 'product__in',
                  'proyecto': 'project', 'desde': 'date_entry_project__gte', 'hasta': 'date_entry_project__lte'}

    filter_kwargs = filterBy(parameters, request)
    result = ProjectContact.objects.filter(**filter_kwargs) \
        .values('contact__country', 'contact__country__x',
                'contact__country__y',
                'contact__country__name',
                'contact__country__name_es',
                'contact__country__name_fr') \
        .order_by('contact__country') \
        .annotate(
        f=Count('contact', filter=Q(contact__sex='F')),
        m=Count('contact', filter=Q(contact__sex='M')))

    pais_array = []
    paisesDetalles = []

    for row in result:
        if 'contact__country' in row:
            row['total'] = row['f'] + row['m']
            paisesDetalles.append({
                'pais_en_ingles': row['contact__country__name'],
                'total': row['total'],
                'f': row['f'],
                'm': row['m'],
                'coordenada_x': row['contact__country__x'],
                'coordenada_y': row['contact__country__y'],
                'pais_en_espaniol': row['contact__country__name_es'],
                'pais_en_frances': row['contact__country__name_fr'],
                'country': row['contact__country'],
                'eventos': "123",
            })
            pais_array.append([
                row['contact__country__name'],
                row['total'],
                row['f'],
                row['m'],
                row['contact__country__x'],
                row['contact__country__y'],
                row['contact__country__name_es'],
                str(row['contact__country']).lower(),
            ])

    return JsonResponse({'pais': list(paisesDetalles), 'paisArray': pais_array})


@csrf_exempt
@login_required
def graficoPaisEventos(request):
    parameters = {'paises[]': 'project__countries__in', 'rubros[]': 'product__in',
                  'proyecto': 'project', 'desde': 'date_entry_project__gte', 'hasta': 'date_entry_project__lte'}

    filter_kwargs = filterBy(parameters, request)

    result = ProjectContact.objects.filter(**filter_kwargs).order_by('project__countries') \
        .values('project__countries', 'project__countries__x', 'project__countries__y',
                'project__countries__name', 'project__countries__name_es',
                'project__countries__name_fr') \
        .annotate(
        f=Count('contact', filter=Q(contact__sex='F')),
        m=Count('contact', filter=Q(contact__sex='M')),
    )

    pais_array = []
    paisesDetalles = []
    for row in result:
        if 'project__countries' in row and row['project__countries__name'] is not None:
            row['total'] = row['f'] + row['m']
            if row['total'] > 0:
                paisesDetalles.append({
                    'pais_en_ingles': row['project__countries__name'],
                    'total': row['total'],
                    'f': row['f'],
                    'm': row['m'],
                    'coordenada_x': row['project__countries__x'],
                    'coordenada_y': row['project__countries__y'],
                    'pais_en_espaniol': row['project__countries__name_es'],
                    'pais_en_frances': row['project__countries__name_fr'],
                    'country': row['project__countries'],
                    'eventos': "123",
                })
                pais_array.append([
                    row['project__countries__name'],
                    row['total'],
                    row['f'],
                    row['m'],
                    row['project__countries__x'],
                    row['project__countries__y'],
                    row['project__countries__name'],
                    str(row['project__countries']).lower(),
                    123
                ])

    return JsonResponse({'pais': list(paisesDetalles), 'paisArray': pais_array})


def filterBy(parameters, request):
    paises = request.POST.getlist('paises[]')
    rubros = request.POST.getlist('rubros[]')
    paisesTodos = True if request.POST['paises_todos'] == '1' else False
    rubrosTodos = True if request.POST['rubros_todos'] == '1' else False
    filter_kwargs = {}

    for key, value in request.POST.items():
        if key in parameters:
            if key == 'paises[]' and paisesTodos == False:
                filter_kwargs[parameters[key]] = paises
            elif key == 'rubros[]' and rubrosTodos == False:
                filter_kwargs[parameters[key]] = rubros
            elif key != 'paises[]' and key != 'rubros[]':
                filter_kwargs[parameters[key]] = value

    return filter_kwargs
