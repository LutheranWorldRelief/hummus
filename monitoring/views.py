from os.path import basename

from django.db.models import Sum, Count, Q, Value, CharField, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

from django_tables2 import RequestConfig
from django_tables2.export.views import ExportMixin
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from openpyxl.utils.cell import coordinate_from_string, column_index_from_string

from .tables import *
from .models import *
from .common import months, JSONResponseMixin
from .common import get_localized_name as __


class ReportExport(LoginRequiredMixin, TemplateView):
    template_name = 'report_export.html'


class DownloadTemplate(LoginRequiredMixin, View):
    def get(self, request):
        # get localized excel tempalte
        obj = Template.objects.get(id='clean-template')
        tfile = getattr(obj, __('file'))
        tfilename = tfile.name


        # loads 'catalogo'
        wb = load_workbook(filename = tfile)
        ws = wb.create_sheet(__('catalog'))

        # initializes data validations
        dvs = {}

        # catalog_cols = (SubProject, Organization, Sex, Educacion, Country, Departament, Comunity, Product, ContactType) TODO: qué pasó con Departamento y Comunity?
        catalog_cols = (SubProject, Organization, Sex, Education, Country, Product, ContactType)
        col_start = 1
        row_start = 1
        for col, col_value in enumerate(catalog_cols, start=col_start):
            ws.cell(row=row_start, column=col, value=col_value.__name__)
        row_start = 2
        for col, col_value in enumerate(catalog_cols, start=col_start):
            if hasattr(col_value.objects, 'for_user'):
                rows = col_value.objects.for_user(request.user).all()
            else:
                rows = col_value.objects.all()
            for row, row_value in enumerate(rows, start=row_start):
                ws.cell(row=row, column=col, value=getattr(row_value, __('name')))
            letter = get_column_letter(col)
            dvs[col_value.__name__] = DataValidation(type="list", allow_blank=True, showDropDown=False, formula1="catalog!$%s$2:$%s$%s" % (letter, letter, row), )
            col += 1


        # applies validations
        ws = wb.get_sheet_by_name(_('data'))
        ws = wb.active
        validation_cols = {'A': 'SubProject', 'B': 'Organization', 'F': 'Sex', 'H': 'Education', 'M': 'Country', 'Q': 'Product'}
        row_start = 3
        row_max = 2000

        for letter in validation_cols:
            dv = dvs[validation_cols[letter]]
            col = column_index_from_string(letter)
            ws.add_data_validation(dv)
            dv.add('%s%s:%s%s' % (letter, row_start, letter, row_max))
            print(dv)
            print('%s%s:%s%s' % (letter, row_start, letter, row_max))


        # resposne
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % (basename(tfilename),)
        return response


class ValidateDupesDoc(LoginRequiredMixin, TemplateView):
    template_name = 'dupes_document.html'


class ValidateDupesName(LoginRequiredMixin, TemplateView):
    template_name = 'dupes_name.html'


class SubProjectTableView(LoginRequiredMixin, PagedFilteredTableView):
    model = SubProject
    table_class = SubProjectTable
    template_name = 'table.html'
    paginate_by = 50
    filter_class = SubProjectFilter
    formhelper_class = SubProjectFilterFormHelper


class ProjectTableView(LoginRequiredMixin, PagedFilteredTableView):
    model = Project
    table_class = ProjectTable
    template_name = 'table.html'
    paginate_by = 50
    filter_class = ProjectFilter
    formhelper_class = ProjectFilterFormHelper


class ContactTableView(LoginRequiredMixin, PagedFilteredTableView):
    model = Contact
    table_class = ContactTable
    template_name = 'table.html'
    paginate_by = 50
    filter_class = ContactFilter
    formhelper_class = ContactFilterFormHelper


class ProjectContactTableView(LoginRequiredMixin, ReportExportMixin, PagedFilteredTableView):
    model = ProjectContact
    table_class = ProjectContactTable
    template_name = 'table.html'
    paginate_by = 50
    filter_class = ProjectContactFilter
    formhelper_class = ProjectContactFilterFormHelper


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


class ContactDetailView(DetailView):
    model = Contact

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
