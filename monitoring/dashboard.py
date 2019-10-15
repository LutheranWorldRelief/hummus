"""
monitoring public dashboard views
"""
from datetime import date

from django.utils.timezone import now
from django.db.models.functions import ExtractYear
from django.db.models import Count, Q, CharField, Case, Value, When
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt

from .models import Project, ProjectContact, Filter
from .common import domain_required, get_localized_name as __


@csrf_exempt
@domain_required()
def get_proyecto(request):
    project_id = request.POST.get('proyecto')
    if project_id:
        proyecto = Project.objects.values().get(id=project_id)
        data = {'proyecto': proyecto}
    else:
        data = {'proyecto': None}
    return JsonResponse(data)


@csrf_exempt
@domain_required()
def cantidad_paises(request):
    parameters = {'paises[]': 'project__countries__in', 'rubros[]': 'project__product__in',
                  'proyecto': 'project_id', 'desde': 'date_entry_project__gte',
                  'hasta': 'date_entry_project__lte'}
    filter_kwargs = filter_by(parameters, request)
    paises = ProjectContact.objects.filter(
        **filter_kwargs).values('project__countries__id').distinct().count()
    data = {'cantidad_paises': paises}
    return JsonResponse(data)


@csrf_exempt
@domain_required()
def cantidad_participantes(request):
    parameters = {'paises[]': 'project__countries__in', 'rubros[]': 'project__product__in',
                  'proyecto': 'project_id', 'desde': 'date_entry_project__gte',
                  'hasta': 'date_entry_project__lte'}
    filter_kwargs = filter_by(parameters, request)
    participantes = ProjectContact.objects.filter(
        **filter_kwargs).values('contact_id').distinct().count()
    data = {'participantes': participantes}
    return JsonResponse(data)


@csrf_exempt
@domain_required()
def cantidad_proyectos(request):
    parameters = {'paises[]': 'project__countries__in', 'rubros[]': 'project__product__in',
                  'proyecto': 'project_id', 'desde': 'date_entry_project__gte',
                  'hasta': 'date_entry_project__lte'}
    filter_kwargs = filter_by(parameters, request)
    proyectos = ProjectContact.objects.filter(
        **filter_kwargs).values('project_id').distinct().count()
    data = {'proyectos': proyectos}
    return JsonResponse(data)


@csrf_exempt
@domain_required()
def get_paises(request):
    paises_todos = (request.POST.get('paises_todos') == 'true')
    ninguno = not (request.POST.getlist("paises[]") or paises_todos)
    parameters = {'proyecto': 'project', 'desde': 'date_entry_project__gte',
                  'hasta': 'date_entry_project__lte'}
    filter_kwargs = filter_by(parameters, request)
    filter_kwargs['project__countries__isnull'] = False

    result = ProjectContact.objects.filter(**filter_kwargs) \
        .values('project__countries', 'project__countries__name') \
        .order_by('project__countries') \
        .distinct()

    paises = []
    for row in result:
        paises.append({
            'id': row['project__countries'],
            'country': row['project__countries__name'],
            'active': row['project__countries'] in request.POST.getlist("paises[]") or
            paises_todos})

    return JsonResponse({'paises': paises, 'todos': paises_todos, 'ninguno': ninguno, })


@csrf_exempt
@domain_required()
def get_rubros(request):
    rubros_todos = request.POST.get('rubros_todos') == 'true'
    ninguno = not (request.POST.getlist("rubros[]") or rubros_todos)
    proyecto_id = request.POST.get('proyecto')
    filter_kwargs = {'product__isnull': False}

    if proyecto_id:
        filter_kwargs['project_id'] = proyecto_id
    result = ProjectContact.objects.filter(**filter_kwargs).order_by(
        __('product__name')).distinct().values('product_id', __('product__name'))

    for row in result:
        row['rubro'] = row[__('product__name')]
        row['id'] = row['product_id']
        row['active'] = str(row['product_id']) in request.POST.getlist("rubros[]") or rubros_todos
    data = {'rubros': list(result), 'todos': rubros_todos, 'ninguno': ninguno, }

    return JsonResponse(data)


@csrf_exempt
@domain_required()
def grafico_organizaciones(request):
    parameters = {'paises[]': 'contact__country__in', 'rubros[]': 'product__in',
                  'proyecto': 'project', 'desde': 'date_entry_project__gte',
                  'hasta': 'date_entry_project__lte'}
    filter_kwargs = filter_by(parameters, request)  # filter_by(parameters, request)

    organizaciones = ProjectContact.objects \
        .filter(organization__isnull=False) \
        .filter(**filter_kwargs) \
        .order_by('organization_id') \
        .values('organization_id', 'organization__name', 'organization__organization_type_id') \
        .distinct()

    org_list = []

    for row in organizaciones:
        if not row['organization__organization_type_id'] or row['organization__organization_type_id'] == 0:
            parent = 'ne'
        else:
            parent = str(row['organization__organization_type_id'])

        org_list.append({
            'id': row['organization_id'] if row['organization_id'] else 'ne',
            'name': row['organization__name'] if row['organization_id'] else 'NE',
            'parent': parent,
            'value': 1})

    types = ProjectContact.objects.filter(**filter_kwargs) \
        .order_by('organization__organization_type_id') \
        .values('organization__organization_type_id',
                __('organization__organization_type__name')) \
        .distinct()

    types_list = []

    for row in types:
        types_list.append({
            'id': str(row['organization__organization_type_id']) if
            row['organization__organization_type_id'] else 'ne',
            'name': row[__('organization__organization_type__name')] if
            row['organization__organization_type_id'] else 'Sin Tipo'
        })

    color_numero = 0
    colores = ['#B2BB1E', '#00AAA7', '#472A2B', '#DDDF00', '#24CBE5', '#64E572', '#FF9655',
               '#FFF263', '#6AF9C4']
    data_dict = {}
    for row in types_list:
        row['color'] = colores[color_numero % len(colores)]
        color_numero += 1
        row['value'] = 0
        data_dict[row['id']] = row

    for row in org_list:
        data_dict[row['parent']]['value'] += 1

    result = list(data_dict.values()) + org_list

    return JsonResponse({'organizaciones': {'data': result, 'total': len(org_list),
                                            'tipos': data_dict,
                                            'total_categorias': len(data_dict)}})


@csrf_exempt
@domain_required()
def proyectos_metas(request):
    proyecto_id = request.POST.get('proyecto')
    if not proyecto_id:
        return JsonResponse({'proyectos_metas': []})
    proyecto = Project.objects.filter(id=proyecto_id).values('id', 'name', 'targetmen',
                                                             'targetwomen').first()
    result = []
    categorias = []
    serie_meta_h = {'name': _('Goal Men'), 'color': 'rgba(42,123,153,.9)', 'data': [],
                    'pointPadding': 0.3, 'pointPlacement': -0.2}
    serie_meta_f = {'name': _('Goal Women'), 'color': 'rgba(68,87,113,1)', 'data': [],
                    'pointPadding': 0.3, 'pointPlacement': 0.2}
    serie_h = {'name': _('Amount Men'), 'color': 'rgba(255,205,85,.8)', 'data': [],
               'pointPadding': 0.4, 'pointPlacement': -0.2}
    serie_f = {'name': _('Amount Women'), 'color': 'rgba(252,110,81,.8)', 'data': [],
               'pointPadding': 0.4, 'pointPlacement': 0.2}

    categorias.append(proyecto['name'])
    serie_meta_f['data'].append(proyecto['targetwomen'])
    serie_meta_h['data'].append(proyecto['targetmen'])
    totales = ProjectContact.objects.filter(project_id=proyecto['id']).aggregate(
        f=Count('contact', filter=Q(contact__sex='F')),
        m=Count('contact', filter=Q(contact__sex='M')))
    totales['total'] = totales['f'] + totales['m']
    print(totales)
    if proyecto['targetmen'] and proyecto['targetwomen']:
        proyecto['meta_total'] = proyecto['targetmen'] + proyecto['targetwomen']
    else:
        proyecto['meta_total'] = None
    serie_f['data'].append(totales['f'])
    serie_h['data'].append(totales['m'])
    result.append(proyecto)
    result.append(totales)
    series = [serie_meta_h, serie_h, serie_meta_f, serie_f]
    agg_result = {'categorias': categorias, 'series': series, 'data': result}
    return JsonResponse({'proyectos_metas': agg_result})


@csrf_exempt
@domain_required()
def grafico_anio_fiscal(request):
    parameters = {'proyecto': 'project__id', 'desde': 'date_entry_project__gte',
                  'hasta': 'date_entry_project__lte'}
    filter_kwargs = filter_by(parameters, request)
    result = ProjectContact.objects.filter(**filter_kwargs).values(
        type=ExtractYear('project__start')).order_by('type').annotate(
            f=Count('contact', filter=Q(contact__sex='F')),
            m=Count('contact', filter=Q(contact__sex='M')),
            total=Count('contact__sex'))

    return JsonResponse({'fiscal': list(result)})


@csrf_exempt
@domain_required()
def grafico_edad(request):
    parameters = {'proyecto': 'project__id', 'desde': 'date_entry_project__gte',
                  'hasta': 'date_entry_project__lte'}
    filter_kwargs = filter_by(parameters, request)
    groups = Filter.objects.filter(slug='age', start__gte=0)
    named_groups = []
    for group in groups:
        current = now().date()
        min_date = date(current.year - group.end, current.month, current.day)
        max_date = date(current.year - group.start, current.month, current.day)
        filter_kwargs['contact__birthdate__gte'] = min_date
        filter_kwargs['contact__birthdate__lte'] = max_date
        row = ProjectContact.objects.filter(**filter_kwargs).\
            aggregate(f=Count('contact', filter=Q(contact__sex='F')),
                      m=Count('contact', filter=Q(contact__sex='M')))
        row['total'] = row['f'] + row['m']
        row['type'] = group.name
        named_groups.append(row)

    result = named_groups
    return JsonResponse({'edad': result})


@csrf_exempt
@domain_required()
def grafico_educacion(request):
    parameters = {'proyecto': 'project__id', 'desde': 'date_entry_project__gte',
                  'hasta': 'date_entry_project__lte'}
    filter_kwargs = filter_by(parameters, request)

    result = ProjectContact.objects.filter(**filter_kwargs).order_by(
        __('contact__education__name')).values(
            __('contact__education__name')).annotate(
                m=Count('id', filter=Q(contact__sex='M')),
                f=Count('id', filter=Q(contact__sex='F')),
                total=Count('id'))

    for row in result:
        row['type'] = str(row[__('contact__education__name')]) if row[__(
            'contact__education__name')] is not None else 'N/E'
    data = {'educacion': list(result)}
    return JsonResponse(data)


@csrf_exempt
@domain_required()
def grafico_eventos(request):
    return JsonResponse({'foo': 'bar'})


@csrf_exempt
@domain_required()
def grafico_tipo_participante(request):
    parameters = {'proyecto': 'project__id', 'desde': 'date_entry_project__gte',
                  'hasta': 'date_entry_project__lte'}
    filter_kwargs = filter_by(parameters, request)
    result = ProjectContact.objects.filter(**filter_kwargs).order_by(
        __('contact__type__name')).values(__('contact__type__name')).annotate(
            type=Case(When(contact__type__name=None, then=Value('NE')),
                      default=__('contact__type__name'), output_field=CharField()),
            total=Count('contact_id', distinct=True),
            f=Count('contact_id', distinct=True, filter=Q(contact__sex='F')),
            m=Count('contact_id', distinct=True, filter=Q(contact__sex='M')))

    data = list(result)
    return JsonResponse(data, safe=False)


@csrf_exempt
@domain_required()
def grafico_sexo_participante(request):
    parameters = {'paises[]': 'contact__country__in', 'rubros[]': 'product__in',
                  'proyecto': 'project', 'desde': 'date_entry_project__gte',
                  'hasta': 'date_entry_project__lte'}
    filter_kwargs = filter_by(parameters, request)  # filter_by(parameters, request)

    result = ProjectContact.objects.filter(**filter_kwargs).aggregate(
        total=Count('contact_id', distinct=True), f=Count('contact_id', distinct=True,
                                                          filter=Q(contact__sex='F')),
        m=Count('contact_id', distinct=True, filter=Q(contact__sex='M'))
    )
    return JsonResponse(result)


@csrf_exempt
@domain_required()
def grafico_nacionalidad(request):
    parameters = {'paises[]': 'contact__country__in', 'rubros[]': 'product__in',
                  'proyecto': 'project', 'desde': 'date_entry_project__gte',
                  'hasta': 'date_entry_project__lte'}

    filter_kwargs = filter_by(parameters, request)
    result = ProjectContact.objects.filter(**filter_kwargs) \
        .values('contact__country', 'contact__country__x',
                'contact__country__y',
                __('contact__country__name')) \
        .order_by('contact__country') \
        .annotate(
            f=Count('contact', filter=Q(contact__sex='F')),
            m=Count('contact', filter=Q(contact__sex='M')))

    pais_array = []
    paises_detalles = []

    for row in result:
        if 'contact__country' in row:
            row['total'] = row['f'] + row['m']
            paises_detalles.append({
                'pais_en_ingles': row[__('contact__country__name')],
                'total': row['total'],
                'f': row['f'],
                'm': row['m'],
                'coordenada_x': row['contact__country__x'],
                'coordenada_y': row['contact__country__y'],
                'country': row['contact__country'],
                'eventos': "123",
            })
            pais_array.append([
                row[__('contact__country__name')],
                row['total'],
                row['f'],
                row['m'],
                row['contact__country__x'],
                row['contact__country__y'],
                str(row['contact__country']).lower(),
            ])

    return JsonResponse({'pais': list(paises_detalles), 'paisArray': pais_array})


@csrf_exempt
@domain_required()
def grafico_pais_eventos(request):
    parameters = {'paises[]': 'project__countries__in', 'rubros[]': 'product__in',
                  'proyecto': 'project', 'desde': 'date_entry_project__gte',
                  'hasta': 'date_entry_project__lte'}

    filter_kwargs = filter_by(parameters, request)

    result = ProjectContact.objects.filter(**filter_kwargs).order_by('project__countries') \
        .values('project__countries', 'project__countries__x', 'project__countries__y',
                __('project__countries__name')) \
        .annotate(
            f=Count('contact', filter=Q(contact__sex='F')),
            m=Count('contact', filter=Q(contact__sex='M')),)

    pais_array = []
    paises_detalles = []
    for row in result:
        if 'project__countries' in row and row[__('project__countries__name')] is not None:
            row['total'] = row['f'] + row['m']
            if row['total'] > 0:
                paises_detalles.append({
                    'pais_en_ingles': row[__('project__countries__name')],
                    'total': row['total'],
                    'f': row['f'],
                    'm': row['m'],
                    'coordenada_x': row['project__countries__x'],
                    'coordenada_y': row['project__countries__y'],
                    'country': row['project__countries'],
                    'eventos': "123",
                })
                pais_array.append([
                    row[__('project__countries__name')],
                    row['total'],
                    row['f'],
                    row['m'],
                    row['project__countries__x'],
                    row['project__countries__y'],
                    str(row['project__countries']).lower(),
                    123
                ])

    return JsonResponse({'pais': list(paises_detalles), 'paisArray': pais_array})


def filter_by(parameters, request):
    paises = request.POST.getlist('paises[]')
    rubros = request.POST.getlist('rubros[]')
    paises_todos = request.POST['paises_todos'] == '1'
    rubros_todos = request.POST['rubros_todos'] == '1'
    filter_kwargs = {}

    for key, value in request.POST.items():
        if key in parameters:
            if key == 'paises[]' and not paises_todos:
                filter_kwargs[parameters[key]] = paises
            elif key == 'rubros[]' and not rubros_todos:
                filter_kwargs[parameters[key]] = rubros
            elif key != 'paises[]' and key != 'rubros[]' and value != '':
                filter_kwargs[parameters[key]] = value

    return filter_kwargs
