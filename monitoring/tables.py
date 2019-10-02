from os.path import basename

from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from django_filters import NumberFilter, FilterSet, CharFilter, ModelChoiceFilter
from django_select2.forms import Select2Widget
from django_tables2 import Table, SingleTableView, RequestConfig
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook

from .models import *
from .common import get_localized_name as __
from .catalog import create_catalog


class ReportExportMixin:

    export_name = "table"
    export_trigger_param = "_export"
    exclude_columns = ()

    def table_to_dataset(self, table, exclude_columns):
        dataset = []
        for i, row in enumerate(table.as_values(exclude_columns=exclude_columns)):
            if i == 0:
                continue
            dataset.append(row)
        return dataset

    def get_export_filename(self, export_format):
        return "{}.{}".format(self.export_name, export_format)

    def create_export(self, export_format):

        # get table and create dataset
        table = self.get_table(**self.get_table_kwargs())
        dataset = self.table_to_dataset(table, self.exclude_columns)

        # get localized excel tempalte
        obj = Template.objects.get(id='clean-template')
        tfile = getattr(obj, __('file'))
        tfilename = tfile.name

        # loads 'datos' sheet # TODO rename to 'data'?
        wb = load_workbook(filename = tfile)
        create_catalog(wb, self.request)
        ws = wb[_('data')]

        # adds rows
        #max = ws.max_row
        max = 3 # Force start at row 3
        for row, row_entry in enumerate(dataset,start=1):
            for col, col_entry in enumerate(row_entry, start=1):
                ws.cell(row=row+max-1, column=col, value=col_entry)

        # resposne
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % (basename(tfilename),)
        return response


    def render_to_response(self, context, **kwargs):
        export_format = self.request.GET.get(self.export_trigger_param, None)
        if export_format == "xlsx":
            return self.create_export(export_format)

        return super().render_to_response(context, **kwargs)


class PagedFilteredTableView(SingleTableView):
    filter_class = None
    formhelper_class = None
    context_filter_name = 'filter'

    def get_queryset(self, **kwargs):
        if hasattr(self.model.objects, 'for_user'):
            qs = self.model.objects.for_user(self.request.user)
        else:
            qs = super(PagedFilteredTableView, self).get_queryset()

        self.filter = self.filter_class(self.request.GET, request=self.request, queryset=qs)
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
        context['export_formats'] = ('xlsx', )
        return context


#
# Specific tables
#


# ProjectContact

class ProjectContactTable(Table):
    class Meta:
        model = ProjectContact
        fields = ('project', 'organization', 'contact.document', 'contact.first_name', 'contact.last_name', __('contact.sex.name'), 'contact.birthdate', 'contact.education', 'contact.phone', 'contact.men', 'contact.women', 'contact.organization', 'contact.country.name', 'contact.deparment', 'contact.community', 'contact.startdate', 'product')

def projects(request):
    if request is None:
        return Project.objects.none()
    return Project.objects.for_user(request.user).all()

def countries(request):
    if request is None:
        return Country.objects.none()
    return Country.objects.for_user(request.user).all()

def organizations(request):
    if request is None:
        return Organization.objects.none()
    return Organization.objects.for_user(request.user).all()

class ProjectContactFilter(FilterSet):
    contact__name = CharFilter(lookup_expr='icontains')
    project = ModelChoiceFilter(queryset=projects, widget=Select2Widget)
    contact__country = ModelChoiceFilter(queryset=countries, widget=Select2Widget)
    organization = ModelChoiceFilter(queryset=organizations, widget=Select2Widget)

    class Meta:
        model = ProjectContact
        fields = ('contact__country', 'project', 'organization', 'contact__name')

class ProjectContactFilterFormHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(
        'contact__country',
        'project',
        'organization',
        'contact__name',
        Submit('submit', 'Apply Filter'),
    )


# Contact

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


# Project

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


# SubProject

class SubProjectTable(ProjectTable):
    class Meta:
        fields = ('name',)
        model = SubProject

class SubProjectFilter(ProjectFilter):
    class Meta:
        fields = ('name',)
        model = SubProject

class SubProjectFilterFormHelper(ProjectFilterFormHelper):
    pass
