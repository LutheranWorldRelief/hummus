from django.db.models import Sum, Count, Q, Value, CharField, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView

from .tables import *
from .models import *
from .common import months, JSONResponseMixin
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

class JsonListView(JSONResponseMixin, TemplateView):

    queryset = None

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, safe=False, **response_kwargs)

    def get(self, request, *args, **kwargs):
        result = {}
        for row in self.queryset:
            result[row.id] = row.name
        return self.render_to_response(result)
