from django.db.models import Sum, Count, Q, Value, CharField, F
from django.db.models.functions import Upper, Lower, Trim
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from .tables import *
from .models import *
from .common import months, JSONResponseMixin, RegexpReplace
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
        queryset = Contact.objects.filter(name__iexact=self.kwargs['name']).values()
        context = {'models': list(queryset) }
        return context


class ContactDocDupes(JSONResponseMixin, TemplateView):
    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get_data(self, context, **kwargs):
        context = {}
        queryset = Contact.objects.filter(document__isnull=False).exclude(document='').values('document').order_by('document').annotate(cuenta=Count('document')).filter(cuenta__gt=1)
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
        context = {'models': list(queryset) }
        return context


class JsonIdName(JSONResponseMixin, TemplateView):

    queryset = None

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get(self, request, *args, **kwargs):
        result = {}
        for row in self.queryset:
            result[row.id] = row.name
        return self.render_to_response(result)


