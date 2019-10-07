from django.db.models import Sum, Count, Q, Value, CharField, F
from django.db.models.functions import Upper, Lower, Trim
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from .tables import *
from .models import *
from .common import months, JSONResponseMixin, RegexpReplace, getPostArray
from .common import get_localized_name as __


class ContactEmpty(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get_data(self, context, **kwargs):
        context = {}
        for f in Contact._meta.fields:
            context[f.name] = None
        return context


class ContactLabels(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

    def get_data(self, context, **kwargs):
        context = {}
        for f in Contact._meta.fields:
            context[f.name] = f.verbose_name
        return context


class ContactNameDupes(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context, **kwargs):
        context = {}
        qs = Contact.objects.annotate(name_uc=Trim(Upper(RegexpReplace(F('name'), r'\s+', ' ', 'g'))))
        queryset = qs.values('name_uc').order_by('name_uc').annotate(cuenta=Count('name_uc')).filter(cuenta__gt=1)
        for row in queryset:
            row['name'] = row['name_uc']
        context = list(queryset)
        return context


class ContactNameDupesDetails(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context, **kwargs):
        context = {}
        qs = Contact.objects.annotate(name_uc=Trim(Upper(RegexpReplace(F('name'), r'\s+', ' ', 'g'))))
        queryset = qs.filter(name_uc=self.kwargs['name']).values()
        context = {'models': list(queryset)}
        return context


class ContactDocDupes(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context, **kwargs):
        context = {}
        queryset = Contact.objects.filter(document__isnull=False).exclude(document='').values('document').order_by(
            'document').annotate(cuenta=Count('document')).filter(cuenta__gt=1)
        for row in queryset:
            row['name'] = ','.join(Contact.objects.filter(document=row['document']).values_list('name', flat=True))
        context = list(queryset)
        return context


class ContactDocDupesDetails(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context, **kwargs):
        context = {}
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
                if row[f.column] and row[f.column] not in values[f.column]:  # TODO strip if string
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
        id = request.POST.get('id')
        ids = request.POST.getlist('ids[]')
        values = getPostArray('values', request.POST)
        context = {}

        contacts = Contact.objects.filter(id__in=ids).exclude(id=id)
        contact = Contact.objects.get(id=id)

        if len(contacts) < 1:
            context['error'] = _('Not enough records to merge.')
            return self.render_to_response(context, status=500)

        if not id in ids:
            context['error'] = _('Selected record not found.')
            return self.render_to_response(context, status=500)

        contact.name = contact.name.strip().replace('  ', ' ')
        if contact.first_name:
            contact.first_name = contact.first_name.strip().replace('  ', ' ')
        if contact.last_name:
            contact.last_name = contact.last_name.strip().replace('  ', ' ')

        contact.save()
        result = None
        for row in contacts:
            result['Proyectos-Contactos'][row.id] = ProjectContact.filter(contact_id=row.id).update(
                contact_id=contact.id)
            result['Eliminado'][row.id] = row.delete()

        context['save'] = saved
        context['result'] = result
        context['id'] = id
        context['model'] = model_to_dict(contact)
        context['models'] = list(contacts.values())
        return self.render_to_response(context)


class ContactDuples(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context, **kwargs):
        id = self.kwargs['id']
        context = {}
        contact = Contact.objects.filter(id=id).first()

        if not contact:
            context['models'] = {}
            return self.render_to_response(context)

        contactsDuples = Contact.objects.filter(Q(name=contact.name) | Q(document=contact.document)).exclude(id=id)

        context['models'] = contactsDuples

        return self.render_to_response(context)


class JsonIdName(JSONResponseMixin, TemplateView):
    queryset = None

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get(self, request, *args, **kwargs):
        result = {}
        for row in self.queryset:
            result[row.id] = row.name
        return self.render_to_response(result)
