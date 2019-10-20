"""
Django views returning json
"""

from django.db.models import Count, Q, F
from django.db.models.functions import Upper, Trim
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import Contact, ProjectContact
from .common import JSONResponseMixin, RegexpReplace, get_post_array


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


class ContactNameDupes(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context):
        parameters = {'countryCode': 'country_id',
                      'projectId': 'projectcontact__project_id',
                      'organizationId': 'organization_id',
                      'nameSearch': 'name__icontains'}
        filter_kwargs = filter_by(parameters, self.request)
        qs = Contact.objects.filter(**filter_kwargs).annotate(
            name_uc=Trim(Upper(RegexpReplace(F('name'), r'\s+', ' ', 'g'))))
        queryset = qs.values('name_uc').order_by('name_uc').annotate(
            cuenta=Count('name_uc')).filter(cuenta__gt=1)
        for row in queryset:
            row['name'] = row['name_uc']
        context = list(queryset)
        return context


class ContactNameDupesDetails(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context):
        qs = Contact.objects.annotate(
            name_uc=Trim(Upper(RegexpReplace(F('name'), r'\s+', ' ', 'g'))))
        queryset = qs.filter(name_uc=self.kwargs['name']).values()
        context = {'models': list(queryset)}
        return context


class ContactDocDupes(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context):
        parameters = {'countryCode': 'country_id',
                      'projectId': 'projectcontact__project_id',
                      'organizationId': 'organization_id',
                      'nameSearch': 'name__icontains'}
        filter_kwargs = filter_by(parameters, self.request)
        queryset = Contact.objects.filter(**filter_kwargs).filter(
            document__isnull=False).exclude(document='').values('document').order_by(
            'document').annotate(cuenta=Count('document')).filter(cuenta__gt=1)
        for row in queryset:
            row['name'] = ','.join(Contact.objects.filter(
                document=row['document']).values_list('name', flat=True))
        context = list(queryset)
        return context


class ContactDocDupesDetails(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context):
        queryset = Contact.objects.filter(document=self.kwargs['document']).values()
        context = {'models': list(queryset)}
        return context


@method_decorator(csrf_exempt, name='dispatch')
class ContactNameValues(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def post(self, request, *args, **kwargs):
        ids = request.POST.getlist('ids[]')
        queryset = Contact.objects.filter(id__in=ids).values()

        values = {}
        for f in Contact._meta.fields:
            if f.column == 'id':
                continue
            values[f.column] = []
            for row in queryset:
                if row[f.column] and row[f.column] not in values[f.column] \
                        and isinstance(values[f.column], str):
                    values[f.column].append(row[f.column].strip())
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
        contacts = Contact.objects.filter(id__in=ids).exclude(id=contact_id)
        contact = Contact.objects.get(id=contact_id)

        if len(contacts) < 1:
            context['error'] = _('Not enough records to merge.')
            return self.render_to_response(context, status=500)

        if contact_id not in ids:
            context['error'] = _('Selected record not found.')
            return self.render_to_response(context, status=500)

        contact.name = contact.name.strip().replace('  ', ' ')
        if contact.first_name:
            contact.first_name = contact.first_name.strip().replace('  ', ' ')
        if contact.last_name:
            contact.last_name = contact.last_name.strip().replace('  ', ' ')

        if not contact.birthdate and values['birthdate'] != '':
            contact.birthdate = values['birthdate']

        if values['document'].strip() != '':
            contact.document = values['document'].strip()

        if values['organization_id'].strip() != '':
            contact.organization_id = int(values['organization_id'])

        if values['sex_id'].strip() != '':
            contact.sex_id = values['sex_id']

        if values['type_id'].strip() != '':
            contact.type_id = values['type_id']

        if values['education_id'].strip() != '':
            contact.education_id = values['education_id']

        if values['phone_work'].strip() != '':
            contact.phone_work = values['phone_work']

        if values['phone_personal'].strip() != '':
            contact.phone_personal = values['phone_personal']

        if values['men_home'].strip() != '':
            contact.men_home = values['men_home']

        if values['women_home'].strip() != '':
            contact.women_home = values['women_home']

        contact.updated_user = request.user.username
        contact.save()

        result = {}
        result['Proyectos-Contactos'] = {}
        result['Eliminado'] = {}
        for row in contacts:
            result['Proyectos-Contactos'][row.id] = ProjectContact.objects.filter(
                contact_id=row.id).update(contact_id=contact.id)
            result['Eliminado'][row.id] = row.delete()

        context['save'] = True
        context['result'] = result
        context['id'] = contact_id
        context['model'] = model_to_dict(contact)
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

        contacts_dupes = Contact.objects.filter(
            Q(name=contact.name) | Q(document=contact.document)).exclude(id=contact_id).values()

        context['models'] = list(contacts_dupes)

        return context


class JsonIdName(JSONResponseMixin, TemplateView):
    """
    return json dict with 'id' as key and 'name' as value
    """

    queryset = ()

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get(self, request, *args, **kwargs):
        result = {}
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
