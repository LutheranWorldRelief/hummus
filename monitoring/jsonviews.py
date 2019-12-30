"""
Django views returning json
"""

from django.db.models import Count, Q, F
from django.db.models.functions import Upper, Trim
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView

from Levenshtein import distance

from .models import Contact, ProjectContact, SubProject, Project
from .common import JSONResponseMixin, RegexpReplace, get_post_array, xstr


class ContactEmpty(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get_data(self, context):
        context = {}
        for f in Contact._meta.fields:
            context[f.name] = None
        return context


class ContactLabels(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get_data(self, context):
        context = {}
        for f in Contact._meta.fields:
            context[f.name] = f.verbose_name
        return context


class ContactNameFuzzyDupes(JSONResponseMixin, TemplateView):
    """Provides list of duplicated based on having a similar name"""

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context):
        context = []
        parameters = {'countryCode': 'country_id',
                      'projectId': 'projectcontact__project_id',
                      'organizationId': 'organization_id',
                      'nameSearch': 'name__icontains'}
        filter_kwargs = filter_by(parameters, self.request)
        if self.request.user and (self.request.user.profile.has_filters() or filter_kwargs):
            contacts = Contact.objects.all()
            contacts = contacts.for_user(self.request.user)
        else:
            context = {'nofilters': True}
            return context
        contacts = contacts.filter(**filter_kwargs).annotate(
            name_uc=Trim(Upper(RegexpReplace(F('name'), r'\s+', ' ', 'g'))))

        # manually (python) counts dupes, because count messed up the distinct() filter
        dupes_list = []
        counter = 0
        for row in contacts:
            counter += 1
            counter2 = 0
            for row2 in contacts:
                counter2 += 1
                if counter2 <= counter:
                    continue
                if len(row.name_uc) < 2 or len(row2.name_uc) < 2:
                    continue
                if (row.name_uc[0] != row2.name_uc[0]) or (row.name_uc[1] != row2.name_uc[1]):
                    continue
                if distance(row.name_uc, row2.name_uc) <= 2:
                    dupes_list.append({'name1': row.name, 'name2': row2.name, 'id1': row.id,
                                       'id2': row2.id})

        context = dupes_list
        return context


class ContactNameDupes(JSONResponseMixin, TemplateView):
    """Provides list of duplicated based on having the exact same name"""

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context):
        parameters = {'countryCode': 'country_id',
                      'projectId': 'projectcontact__project_id',
                      'organizationId': 'organization_id',
                      'nameSearch': 'name__icontains'}
        filter_kwargs = filter_by(parameters, self.request)
        if self.request.user and (self.request.user.profile.has_filters() or filter_kwargs):
            contacts = Contact.objects.all()
            contacts = contacts.for_user(self.request.user)
        else:
            context = {'nofilters': True}
            return context
        contacts = contacts.filter(**filter_kwargs).annotate(
            name_uc=Trim(Upper(RegexpReplace(F('name'), r'\s+', ' ', 'g'))))

        # manually (python) counts dupes, because count messed up the distinct() filter
        names = {}
        for row in contacts:
            if row.name_uc not in names:
                names[row.name_uc] = 0
            names[row.name_uc] += 1

        # removes non dupes and prepares list
        dupes = dict(filter(lambda k_v: k_v[1] > 1, names.items()))
        dupes_list = []
        for row in dupes:
            dupes_list.append({'name': row, 'count': dupes[row]})
        context = dupes_list
        return context


class ContactNameDupesDetails(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context):
        qs = Contact.objects.annotate(
            name_uc=Trim(Upper(RegexpReplace(F('name'), r'\s+', ' ', 'g'))))
        qs = qs.filter(name_uc=self.kwargs['name']).values()

        # make Point JSON serializable
        for row in qs:
            if row['location']:
                row['location'] = row['location'].coords

        context = {'models': list(qs)}
        return context


class ContactIdsDupesDetails(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context):
        qs = Contact.objects.filter(id__in=(self.kwargs['id1'], self.kwargs['id2'])).values()

        # make Point JSON serializable
        for row in qs:
            if row['location']:
                row['location'] = row['location'].coords

        context = {'models': list(qs)}
        return context


class ContactDocDupes(JSONResponseMixin, TemplateView):
    """Provides list of duplicated based on having the exact same document"""

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context):
        parameters = {'countryCode': 'country_id',
                      'projectId': 'projectcontact__project_id',
                      'organizationId': 'organization_id',
                      'nameSearch': 'name__icontains'}
        filter_kwargs = filter_by(parameters, self.request)
        contacts = Contact.objects.all()
        if self.request.user:
            contacts = contacts.for_user(self.request.user)

        # manually (python) counts dupes, because count messed up the distinct() filter
        contacts = contacts.filter(**filter_kwargs).filter(document__isnull=False).\
            exclude(document='')
        docs = {}
        for row in contacts:
            if row.document not in docs:
                docs[row.document] = 0
            docs[row.document] += 1

        # removes non dupes and prepares list
        dupes = dict(filter(lambda k_v: k_v[1] > 1, docs.items()))
        dupes_list = []
        for row in dupes:
            dupes_list.append({'document': row, 'cuenta': dupes[row]})

        # gets names of dupes with same document
        for row in dupes_list:
            row['name'] = ', '.join(Contact.objects.filter(
                document=row['document']).values_list('name', flat=True))
        context = dupes_list
        return context


class ContactDocDupesDetails(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context):
        queryset = Contact.objects.filter(document=self.kwargs['document']).values()
        for row in queryset:
            if row['location']:
                row['location'] = row['location'].coords
        context = {'models': list(queryset)}
        return context


@method_decorator(csrf_exempt, name='dispatch')
class ContactNameValues(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def post(self, request, *args, **kwargs):
        ids = request.POST.getlist('ids[]')
        queryset = Contact.objects.filter(id__in=ids).values()

        for row in queryset:
            if row['location']:
                row['location'] = row['location'].coords

        values = {}
        for f in Contact._meta.fields:
            if f.column == 'id':
                continue
            values[f.column] = []
            for row in queryset:
                if row[f.column] and row[f.column] not in values[f.column] \
                        and isinstance(values[f.column], str):
                    values[f.column].append(xstr(row[f.column]))
                else:
                    values[f.column].append(row[f.column])

        resolve = {}
        for value in values:
            if len(values[value]) == 1:
                values[value] = values[value][0]
            elif len(values[value]) == 0:
                values[value] = None
            else:
                resolve[value] = values[value]

        context = {}
        context['ids'] = ids
        context['values'] = values
        context['resolve'] = resolve
        return self.render_to_response(context)


@method_decorator(csrf_exempt, name='dispatch')
class ContactFusion(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def post(self, request, *args, **kwargs):
        contact_id = request.POST.get('id')
        ids = request.POST.getlist('ids[]')
        values = get_post_array('values', request.POST)
        context = {}

        # all contacts to be deleted
        contacts = Contact.objects.filter(id__in=ids).exclude(id=contact_id)

        # the contact to remain, the chosen one
        contact = Contact.objects.get(id=contact_id)

        if len(contacts) < 1:
            context['error'] = _('Not enough records to merge.')
            return self.render_to_response(context, status=500)

        if contact_id not in ids:
            context['error'] = _('Selected record not found.')
            return self.render_to_response(context, status=500)

        contact.name = xstr(contact.name)
        if contact.first_name:
            contact.first_name = xstr(contact.first_name)
        if contact.last_name:
            contact.last_name = xstr(contact.last_name)

        if not contact.birthdate and values['birthdate'] != '':
            contact.birthdate = values['birthdate']

        if xstr(values['document']) != '':
            contact.document = xstr(values['document'])

        if xstr(values['organization_id']) != '':
            contact.organization_id = int(xstr(values['organization_id']))

        if xstr(values['sex_id']) != '':
            contact.sex_id = xstr(values['sex_id'])

        if xstr(values['contact_type_id']) != '':
            contact.contact_type_id = xstr(values['contact_type_id'])

        if xstr(values['education_id']) != '':
            contact.education_id = xstr(values['education_id'])

        if xstr(values['phone_work']) != '':
            contact.phone_work = xstr(values['phone_work'])

        if xstr(values['phone_personal']) != '':
            contact.phone_personal = xstr(values['phone_personal'])

        if xstr(values['men_home']) != '':
            contact.men_home = xstr(values['men_home'])

        if xstr(values['women_home']) != '':
            contact.women_home = xstr(values['women_home'])

        contact.updated_user = request.user.username
        contact.save()

        contact_dict = model_to_dict(contact)
        if contact.location:
            contact_dict['location'] = contact.location.coords

        result = {}
        result['Proyectos-Contactos'] = {}
        result['Eliminado'] = {}
        for row in contacts:
            # avoid unique together (contact, project) constraint
            result['Proyectos-Contactos'][row.id] = 0
            # gets participations of contact to be deleted
            their_projects = ProjectContact.objects.filter(contact_id=row.id)
            for project_contact in their_projects:
                # updates to use chosen-one, if he is not already participating
                if not ProjectContact.objects.filter(project_id=project_contact.project_id,
                    contact_id=contact.id).exists():
                    project_contact.contact_id=contact.id
                    project_contact.save()
                    result['Proyectos-Contactos'][row.id] += 1
            result['Eliminado'][row.id] = row.delete()

        context['save'] = True
        context['result'] = result
        context['id'] = contact_id
        context['model'] = contact_dict
        context['models'] = list(contacts.values())
        return self.render_to_response(context)


class ContactImportDupes(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context):
        contact_id = self.kwargs['id']
        context = {}
        contact = Contact.objects.filter(id=contact_id).first()

        if not contact:
            context['models'] = {}
            return context
        condition = Q(name__iexact=contact.name)
        if contact.document:
            condition = (condition | Q(document__iexact=contact.document))
        contacts_dupes = Contact.objects.filter(condition).values()

        # make Point JSON serializable
        for row in contacts_dupes:
            if row['location']:
                row['location'] = row['location'].coords

        context['models'] = list(contacts_dupes)

        return context


class YearsAPI(JSONResponseMixin, TemplateView):
    """
    List of years used in projects
    """

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_context_data(self, **kwargs):
        queryset = Project.objects.order_by('start__fyear').\
            values_list('start__fyear', flat=True).distinct()
        return list(queryset)


class ProjectContactCounter(JSONResponseMixin, TemplateView):
    """
    Count participants filter by several params
    """

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        queryset = ProjectContact.objects.all()

        if self.request.GET.get('year'):
            year = int(self.request.GET.get('year'))
            queryset = queryset.filter(date_entry_project__fyear=year)
        if self.request.GET.get('quarter'):
            quarter = int(self.request.GET.get('quarter'))
            queryset = queryset.filter(date_entry_project__fquarter=quarter)
        ''  # if self.request.GET.get('lwrregion_id'):
        ''  # queryset = queryset.filter(lwrregion_id=self.request.GET.get('lwrregion_id'))

        ''  # if self.request.GET.get('country_id[]'):
        ''  # queryset = queryset.filter(country_id=self.request.GET.get('country_id[]'))
        if self.request.GET.get('subproject_id'):
            queryset = queryset.filter(project_id=self.request.GET.get('subproject_id'))
        if self.request.GET.get('project_id'):
            queryset = queryset.filter(project_id=self.request.GET.get('project_id'))
        elif self.request.user and hasattr(queryset.model.objects, 'for_user'):
            queryset = queryset.for_user(self.request.user)

        # get totals
        totals = dict(queryset.order_by().values('contact__sex_id').
                      annotate(total=Count('id')).values_list('contact__sex_id', 'total'))

        if totals:
            totals['T'] = totals['M'] + totals['F']
        context['totals'] = totals

        # get totals by year
        query_years = queryset.order_by().\
            values('date_entry_project__fyear', 'contact__sex_id').\
            annotate(total=Count('id')).values('date_entry_project__fyear',
                                               'contact__sex_id', 'total')
        years = {}
        for query_year in query_years:
            fyear = query_year['date_entry_project__fyear']
            if fyear not in years:
                years[fyear] = {}
            current_year = years[fyear]
            current_year[query_year['contact__sex_id']] = query_year['total']
            if 'T' not in current_year:
                current_year['T'] = 0
            current_year['T'] += query_year['total']
        context['year'] = years

        # get totals by quarter
        query_years = queryset.order_by().\
            values('date_entry_project__fyear', 'date_entry_project__fquarter', 'contact__sex_id').\
            annotate(total=Count('id')).values('date_entry_project__fyear',
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
    Countries
    """

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        queryset = ProjectContact.objects.all()

        paises_todos = (self.request.GET.get('paises_todos') == 'true')
        ninguno = not (self.request.GET.getlist("paises[]") or paises_todos)

        if self.request.GET.get('lwrregion_id'):
            queryset = queryset.filter(lwrregion_id=self.request.GET.get('lwrregion_id'))
        if self.request.GET.get('country_id[]'):
            queryset = queryset.filter(id=self.request.GET.get('country_id[]'))
        elif self.request.user and hasattr(queryset.model.objects, 'for_user'):
            queryset = queryset.for_user(self.request.user)

        countries = queryset.filter(project__countries__isnull=False)\
            .order_by('project__countries__id')\
            .distinct('project__countries__id')\
            .values(
            country_id=F('project__countries__id'),
            country_name=F(_('project__countries__name'))
        )
        paises = []
        for row in countries:
            paises.append({
                'id': row['country_id'],
                'name': row['country_name'],
                'active': row['country_id'] in self.request.POST.getlist("paises[]") or
                paises_todos})

        context['paises'] = paises
        context['todos'] = {'todos': paises_todos}

        return context


class ProjectAPIListView(JSONResponseMixin, ListView):
    """
    List of Subproojects using JSON (limit by Project if needed)
    """

    def render_to_response(self, context, **response_kwargs):
        json_context = {}
        json_context['object_list'] = context['object_list']
        return self.render_to_json_response(json_context, safe=False, **response_kwargs)

    def get_queryset(self):
        queryset = Project.objects.all()
        if 'project_id' in self.kwargs:
            queryset = queryset.filter(id=self.kwargs['project_id'])
        elif self.request.user and hasattr(queryset.model.objects, 'for_user'):
            queryset = queryset.for_user(self.request.user)
        return list(queryset.values())


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
        if 'project_id' in self.kwargs:
            queryset = queryset.filter(project_id=self.kwargs['project_id'])
        elif self.request.user and hasattr(queryset.model.objects, 'for_user'):
            queryset = queryset.for_user(self.request.user)
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


def filter_by(parameters, request):
    filter_kwargs = {}

    for key in request.GET:
        if key in parameters:
            value = request.GET[key]
            if value != '' and value.find('-') == -1:
                filter_kwargs[parameters[key]] = value

    return filter_kwargs
