"""
Django views returning json
"""

from django.db.models import Sum, Count, Q, F, FloatField
from django.db.models.functions import Upper, Trim, Cast, Coalesce
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView

from Levenshtein import distance

from .models import Contact, ProjectContact, SubProject, Project, LWRRegion
from .common import JSONResponseMixin, RegexpReplace, get_post_array, xstr


def mydashboard(request, queryset):
    if request.GET.get('mydashboard') and request.user and \
            hasattr(queryset.model.objects, 'for_user'):
        queryset = queryset.for_user(request.user)
    return queryset


class YearsAPI(JSONResponseMixin, TemplateView):
    """
    List of years used in projects
    """

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_context_data(self, **kwargs):
        # FIXME : from first start_fyear to current year would be better
        queryset = Project.objects.order_by('start__fyear').exclude(projectcontact__isnull=True). \
            values_list('start__fyear', flat=True).distinct()
        return list(queryset)


class TargetsCounter(JSONResponseMixin, TemplateView):
    """
    Count projects targets filter by several params
    """

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        queryset = Project.objects.all().order_by()

        # exclude projects with no participants in 3D
        queryset = queryset.exclude(projectcontact__isnull=True)
        men = 'targetmen'
        women = 'targetwomen'

        # filter by selected years
        if self.request.GET.get('year[]'):
            years = self.request.GET.getlist('year[]')
            years_filter = Q()
            for year in years:
                # FIXME: determianr como se cuentan los target por año
                years_filter |= Q(start__fyear__lte=year, end__fyear__gte=year)
            queryset = queryset.filter(years_filter)
        else:
            years = list(Project.objects.order_by('start__fyear').
                         exclude(projectcontact__isnull=True).
                         values_list('start__fyear', flat=True).distinct())

        if self.request.GET.get('lwrregion_id[]'):
            regions = self.request.GET.getlist('lwrregion_id[]')
            queryset = queryset.filter(lwrregion__id__in=regions)
        if self.request.GET.get('country_id[]'):
            countries = self.request.GET.getlist('country_id[]')
            queryset = queryset.filter(subproject__country__id__in=countries).distinct()

        if self.request.GET.get('subproject_id'):
            subproject = self.request.GET.get('subproject_id')
            queryset = queryset.filter(subproject=subproject)
            # modify target field variable to count subproject not project targets
            men = 'subproject__targetmen'
            women = 'subproject__targetwomen'
        elif self.request.GET.get('project_id'):
            project = self.request.GET.get('project_id')
            queryset = queryset.filter(id=project)
        else:
            queryset = mydashboard(self.request, queryset)

        totals = queryset.aggregate(M=Coalesce(Sum(men), 0),
                                    F=Coalesce(Sum(women), 0))
        totals['T'] = sum(totals.values())
        context['totals'] = totals

        # get totals by year
        years_data = {}
        for year in years:
            # FIXME: determianr como se cuentan los target por año
            year_filter = Q(start__fyear__lte=year, end__fyear__gte=year)
            year_queryset = queryset.filter(year_filter)
            year_total = dict(year_queryset.aggregate(M=Coalesce(Sum('targetmen'), 0),
                                                      F=Coalesce(Sum('targetwomen'), 0)))

            year_total['T'] = sum(year_total.values())
            years_data[year] = year_total
        context['year'] = years_data

        return context


class ProjectContactCounter(JSONResponseMixin, TemplateView):
    """
    Count participants filter by several params
    """

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        queryset = ProjectContact.objects.all().order_by()

        # filter by selected years
        if self.request.GET.get('year[]'):
            years = self.request.GET.getlist('year[]')
            years_filter = Q()
            for year in years:
                years_filter |= Q(project__end__fyear__gte=year,
                                  date_entry_project__fyear__lte=year)
            queryset = queryset.filter(years_filter)
        else:
            years = list(Project.objects.order_by('start__fyear').
                         exclude(projectcontact__isnull=True).
                         values_list('start__fyear', flat=True).distinct())

        if self.request.GET.get('quarter'):
            quarter = int(self.request.GET.get('quarter'))
            queryset = queryset.filter(date_entry_project__fquarter=quarter)
        if self.request.GET.get('lwrregion_id[]'):
            queryset = queryset.filter(
                project__lwrregion__id__in=self.request.GET.getlist('lwrregion_id[]'))
        if self.request.GET.get('from_date'):
            queryset = queryset.filter(
                date_entry_project__gte=self.request.GET.get('from_date'))
        if self.request.GET.get('to_date'):
            queryset = queryset.filter(
                date_entry_project__lte=self.request.GET.get('to_date'))

        if self.request.GET.get('country_id[]'):
            queryset = queryset.filter(
                subproject__country__in=self.request.GET.getlist('country_id[]'))
        if self.request.GET.get('subproject_id'):
            queryset = queryset.filter(subproject_id=self.request.GET.get('subproject_id'))
        if self.request.GET.get('project_id'):
            queryset = queryset.filter(project_id=self.request.GET.get('project_id'))
        else:
            queryset = mydashboard(self.request, queryset)

        # get unique participants # not used for now
        # queryset_unique = queryset.order_by().values('contact', 'contact__sex_id').distinct()

        # get unique totals by gender
        totals = dict(queryset.values_list('contact__sex_id').
                      annotate(total=Count('contact', distinct=True)))

        if totals:
            totals['T'] = sum(totals.values())

        context['totals'] = totals

        # get totals by year
        years_data = {}
        for year in years:
            year_filter = Q(project__end__fyear__gte=year,
                            date_entry_project__fyear__lte=year)
            year_queryset = queryset.filter(year_filter)
            year_total = dict(year_queryset.values_list('contact__sex_id').
                              annotate(total=Count('contact', distinct=True)))

            year_total['T'] = sum(year_total.values())
            years_data[year] = year_total
        context['year'] = years_data

        # get totals by quarter
        query_years = queryset. \
            values('date_entry_project__fyear',
                   'date_entry_project__fquarter',
                   'contact__sex_id'). \
            annotate(total=Count('contact', distinct=True)). \
            values('date_entry_project__fyear',
                   'date_entry_project__fquarter',
                   'contact__sex_id', 'total')
        years = {}
        for query_year in query_years:
            fy_quarter = "{}Q{}".format(query_year['date_entry_project__fyear'],
                                        query_year['date_entry_project__fquarter'])
            if fy_quarter not in years:
                years[fy_quarter] = {}
            current_year = years[fy_quarter]
            current_year[query_year['contact__sex_id']] = query_year['total']
            if 'T' not in current_year:
                current_year['T'] = 0
            current_year['T'] += query_year['total']
        context['quarters'] = years

        return context


class Countries(JSONResponseMixin, TemplateView):
    """
    List of countries with projects and participants
    """

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        queryset = ProjectContact.objects.all()

        countries_id = self.request.GET.getlist('country_id[]')
        regions = self.request.GET.getlist('lwrregion_id[]')
        project = self.request.GET.get('project_id')
        from_date = self.request.GET.get('from_date')
        to_date = self.request.GET.get('to_date')
        years = self.request.GET.getlist('year[]')

        if len(regions) > 0 or regions:
            queryset = queryset.filter(project__lwrregion__id__in=regions)
        if len(years) > 0 or years:
            queryset = queryset.filter(date_entry_project__fyear__in=years)

        if from_date:
            queryset = queryset.filter(date_entry_project__gte=from_date)
        if to_date:
            queryset = queryset.filter(date_entry_project__lte=to_date)

        if project:
            queryset = queryset.filter(project_id=project)
        else:
            queryset = mydashboard(self.request, queryset)

        countries = queryset.exclude(project__countries__isnull=True) \
            .values(country_id=F('project__countries__id'),
                    country_name=F(_('project__countries__name')),
                    region=F('project__lwrregion__id')) \
            .order_by('project__countries__name').distinct()

        paises = []
        for row in countries:
            new_row = {
                'id': row['country_id'],
                'name': row['country_name'],
                'region': row['region'],
                'active': row['country_id'] in countries_id,
            }
            if self.request.GET.get('extra_counters'):
                new_row['projects'] = Project.objects.filter(
                    countries=row['country_id']).count()
                new_row['subprojects'] = SubProject.objects.filter(
                    country_id=row['country_id']).count()
            paises.append(new_row)

        context['paises'] = paises

        return context


class LWRRegions(JSONResponseMixin, TemplateView):
    """
    Regions
    """

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        queryset = LWRRegion.objects.all()

        regions = self.request.GET.getlist('lwrregion_id[]')
        project = self.request.GET.get('project_id')

        if project:
            queryset = queryset.filter(project__id=project)
        # if self.request.user and hasattr(queryset.model.objects, 'for_user'):
        #    queryset = queryset.for_user(self.request.user)

        lwrregions = queryset.order_by('name').values('id', 'name')

        lwr_regions = []
        for row in lwrregions:
            lwr_regions.append({
                'id': row['id'],
                'name': row['name'],
                'active': row['id'] in regions
            })

        context['regions'] = lwr_regions

        return context


class GeographyAPI(JSONResponseMixin, TemplateView):
    """
    API retorna un JSON con datos de los paises relacionados
    a proyectos implementados tales como ID,Alfa 3,Nombre,
    coordenadas(X,Y) del pais y cantidad de participantes
    por pais segregado por genero
    """

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        queryset = ProjectContact.objects.all()
        project_queryset = Project.objects.all().order_by()
        filter_kwargs = {}

        regions = self.request.GET.getlist('lwrregion_id[]')
        countries = self.request.GET.getlist('country_id[]')
        project = self.request.GET.get('project_id')

        if len(regions) > 0 or regions:
            queryset = queryset.filter(project__lwrregion__id__in=regions)
            filter_kwargs['project__lwrregion__id__in'] = regions

        if len(countries) > 0 or countries:
            queryset = queryset.filter(subproject__country__id__in=countries)
            filter_kwargs['subproject__country__id__in'] = countries
        else:
            queryset = queryset.filter(subproject__country__isnull=False)

        if project:
            queryset = queryset.filter(project_id=project)
            filter_kwargs['project_id'] = project
        else:
            queryset = mydashboard(self.request, queryset)

        countries = queryset.exclude(project__countries__isnull=True) \
            .values(country_id=F('project__countries__id'),
                    alta_3=F('project__countries__alfa3'),
                    country_name=F(_('project__countries__name')),
                    x=Cast(F('project__countries__x'), FloatField()),
                    y=Cast(F('project__countries__y'), FloatField()),
                    ).order_by('project__countries__name').distinct()

        participants = []
        for row in countries:
            ''  # get the target by gender in a country
            targets = project_queryset. \
                filter(subproject__country__id=row['country_id']). \
                aggregate(M=Coalesce(Sum('targetmen'), 0), F=Coalesce(Sum('targetwomen'), 0))
            participants_target = targets['F'] + targets['M']

            ''  # get totals participants by gender in a country
            totals = dict(queryset.order_by().
                          filter(subproject__country__id=row['country_id']).
                          values_list('contact__sex_id').
                          annotate(total=Count('contact', distinct=True))
                          )

            totals['T'] = totals.get('M', 0) + totals.get('F', 0)
            percentage = (totals['T'] / participants_target) * 100
            participants.append({
                'id': row['country_id'],
                'alfa3': row['alta_3'],
                'name': row['country_name'],
                'location': [row['x'], row['y']],
                'total': totals.get('T', 0),
                'total_target': participants_target,
                'women': totals.get('F', 0),
                'target_women': targets.get('F', 0),
                'men': totals.get('M', 0),
                'target_men': targets.get('M', 0),
                'percentage': percentage
            })

        context['participants'] = participants

        return context


class ProjectAPIListView(JSONResponseMixin, ListView):
    """
    List of Subproojects using JSON (limit by Project if needed)
    """

    def render_to_response(self, context, **response_kwargs):
        # json_context = context['object_list']
        json_context = {}
        for row in context['object_list']:
            json_context[row['id']] = row['name']
        return self.render_to_json_response(json_context, safe=False, **response_kwargs)

    def get_queryset(self):
        queryset = Project.objects.all()

        if 'from_date' in self.kwargs:
            queryset = queryset.filter(start__gte=self.kwargs['from_date'])
        if 'to_date' in self.kwargs:
            queryset = queryset.filter(start__lte=self.kwargs['to_date'])

        # filter by selected years
        years_filter = Q()
        if self.request.GET.get('year[]'):
            years = self.request.GET.getlist('year[]')
            for year in years:
                years_filter |= Q(start__fyear__lte=year, end__fyear__gte=year)
            queryset = queryset.filter(years_filter)

        if self.request.GET.get('country_id[]'):
            countries = self.request.GET.getlist('country_id[]')
            queryset = queryset.filter(subproject__country__id__in=countries)

        if 'project_id' in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['project_id'])
        else:
            queryset = mydashboard(self.request, queryset)
        return list(queryset.values('id', 'name'))


class SubProjectAPIListView(JSONResponseMixin, ListView):
    """
    List of Subproojects using JSON (limit by Project if needed)
    """

    def render_to_response(self, context, **response_kwargs):
        json_context = {}
        json_context['object_list'] = context['object_list']
        return self.render_to_json_response(json_context, safe=False, **response_kwargs)

    def get_queryset(self):
        queryset = SubProject.objects.all()
        if 'subproject_id' in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['subproject_id'])

        if 'from_date' in self.kwargs:
            queryset = queryset.filter(start__gte=self.kwargs['from_date'])
        if 'to_date' in self.kwargs:
            queryset = queryset.filter(start__lte=self.kwargs['to_date'])

        # filter by selected years
        years_filter = Q()
        if self.request.GET.get('year[]'):
            years = self.request.GET.getlist('year[]')
            for year in years:
                years_filter |= Q(start__fyear__lte=year, end__fyear__gte=year)
            queryset = queryset.filter(years_filter)

        if self.request.GET.get('country_id[]'):
            countries = self.request.GET.getlist('country_id[]')
            queryset = queryset.filter(country__id__in=countries)

        if 'project_id' in self.kwargs:
            queryset = queryset.filter(project_id=self.kwargs['project_id'])
        else:
            queryset = mydashboard(self.request, queryset)
        return list(queryset.values())


class JsonIdName(JSONResponseMixin, TemplateView):
    """
    return json dict with 'id' as key and 'name' as value
    """

    queryset = ()

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get(self, request, *args, **kwargs):
        result = {}
        if request.user and hasattr(self.queryset.model.objects, 'for_user'):
            self.queryset = self.queryset.for_user(request.user)
        for row in self.queryset:
            result[row.id] = row.name
        return self.render_to_response(result)


