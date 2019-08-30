from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django_tables2 import RequestConfig

from .tables import *
from .models import *

#<<Start Config language >>
from django.conf import settings
from django.contrib.auth import user_logged_in
from django.dispatch import receiver

@receiver(user_logged_in)
def on_user_logged_in(sender, request, **kwargs):
    languageUser = Profile.objects.filter(user_id=request.user.id).values('language')
    if languageUser:
        settings.LANGUAGE_CODE = languageUser[0]['language']
#<<End Config language >>

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
