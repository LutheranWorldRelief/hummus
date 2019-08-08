from django.shortcuts import render
from django.views.generic import TemplateView
from django_tables2 import RequestConfig

from .tables import PagedFilteredTableView, ContactTable, ContactFilter, ContactFilterFormHelper
from .models import Contact

class ContactTableView(PagedFilteredTableView):
    model = Contact
    table_class = ContactTable
    template_name = 'contact_table.html'
    paginate_by = 50
    filter_class = ContactFilter
    formhelper_class = ContactFilterFormHelper
