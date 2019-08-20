from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django_tables2 import RequestConfig

from .tables import *
from .models import *


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
