from django.utils.safestring import mark_safe

from django_tables2 import Table, SingleTableView, RequestConfig
from django_filters import NumberFilter, FilterSet, CharFilter
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit

from .models import *


class PagedFilteredTableView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        qs = super(PagedFilteredTableView, self).get_queryset()
        self.filter = self.filter_class(self.request.GET, queryset=qs)
        self.filter.form.helper = self.formhelper_class()
        return self.filter.qs

    def get_table(self, **kwargs):
        table = super(PagedFilteredTableView, self).get_table()
        if 'page' in self.kwargs:
            page =  self.kwargs['page']
        else:
            page = 1
        RequestConfig(self.request, paginate={'page': page,
                            "per_page": self.paginate_by}).configure(table)
        return table

    def get_context_data(self, **kwargs):
        context = super(PagedFilteredTableView, self).get_context_data()
        context[self.context_filter_name] = self.filter
        return context


#
# Specific tables

class ContactTable(Table):
    def render_name(self, value, record):
        url = record.get_absolute_url()
        return mark_safe('<a href="%s">%s</a>' % (url, record))

    class Meta:
        model = Contact
        fields = ('name', 'country', 'sex')

class ContactFilter(FilterSet):
    class Meta:
        model = Contact
        fields = ('name', 'country', 'sex')

class ContactFilterFormHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(
        'name',
        'country',
        'sex',
        Submit('submit', 'Apply Filter'),
    )


class ProjectTable(Table):
    def render_name(self, value, record):
        url = record.get_absolute_url()
        return mark_safe('<a href="%s">%s</a>' % (url, record))

    class Meta:
        model = Project
        fields = ('name',)

class ProjectFilter(FilterSet):
    name = CharFilter(lookup_expr='icontains')

    class Meta:
        fields = ('name',)
        model = Project

class ProjectFilterFormHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(
        'name',
        Submit('submit', 'Apply Filter'),
    )
