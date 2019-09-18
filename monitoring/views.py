from django.db.models import Sum, Count, Q, Value, CharField, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig

from .tables import *
from .models import *
from .common import months, JSONResponseMixin
from .common import get_localized_name as __


class DownloadTemplate(LoginRequiredMixin, View):
    def get(self, request):
        obj = Template.objects.get(id='clean-template')
        link = getattr(obj, __('file'))
        return redirect("%s/%s" % (settings.MEDIA_URL, link))


class ValidateDupesId(LoginRequiredMixin, TemplateView):
    template_name = 'dupes_id.html'


class SubProjectTableView(LoginRequiredMixin, PagedFilteredTableView):
    model = SubProject
    table_class = SubProjectTable
    template_name = 'contact_table.html'
    paginate_by = 50
    filter_class = SubProjectFilter
    formhelper_class = SubProjectFilterFormHelper


class ProjectTableView(LoginRequiredMixin, PagedFilteredTableView):
    model = Project
    table_class = ProjectTable
    template_name = 'contact_table.html'
    paginate_by = 50
    filter_class = ProjectFilter
    formhelper_class = ProjectFilterFormHelper


class ContactTableView(LoginRequiredMixin, PagedFilteredTableView):
    model = Contact
    table_class = ContactTable
    template_name = 'contact_table.html'
    paginate_by = 50
    filter_class = ContactFilter
    formhelper_class = ContactFilterFormHelper


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['months'] = months
        context['projects'] = Project.objects.values('id', 'name')
        return context


class SubProjectDetailView(DetailView):
    model = SubProject

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class ProjectDetailView(DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
        queryset = Contact.objects.values('name', 'document').annotate(cuenta=Count('document')).filter(cuenta__gt=1)
        context = list(queryset)
        return context
