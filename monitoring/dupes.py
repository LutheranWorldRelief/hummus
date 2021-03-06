"""
Django JSON views used by deduplication
"""

from django.db.models import Q, F
from django.db.models.functions import Upper, Trim
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from Levenshtein import distance

from .models import Contact, ProjectContact
from .common import JSONResponseMixin, RegexpReplace, get_post_array, xstr


def filter_by(parameters, request):
    filter_kwargs = {}

    for key in request.GET:
        if key in parameters:
            value = request.GET[key]
            if value != '' and value.find('-') == -1:
                filter_kwargs[parameters[key]] = value

    return filter_kwargs


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
        contacts = contacts.filter(**filter_kwargs).filter(document__isnull=False). \
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
                    project_contact.contact_id = contact.id
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
