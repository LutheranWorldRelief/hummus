from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django_tables2 import RequestConfig

from .tables import *
from .models import *
from .common import months


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
