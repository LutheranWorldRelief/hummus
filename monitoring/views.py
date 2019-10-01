from os.path import basename

from django.db.models import Sum, Count, Q, Value, CharField, F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, FormView
from django.views.decorators.csrf import csrf_exempt

from django_tables2 import RequestConfig
from django_tables2.export.views import ExportMixin
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook
import pandas as pd

from .tables import *
from .models import *
from .common import DomainRequiredMixin, months, JSONResponseMixin, get_localized_name as __
from .catalog import create_catalog

@method_decorator(csrf_exempt, name='dispatch')
class Capture(TemplateView):

    template_name = 'capture.html'

    def get(self, request):
        context = {}
        context['meta'] = request.META
        context['body'] = request.body
        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        context['meta'] = request.META
        context['body'] = request.body
        row = Request()
        row.meta = request.META
        row.body = request.body
        row.save()
        return render(request, self.template_name, context)



class ImportParticipants(DomainRequiredMixin, FormView):
    def post(self, request):
        excel_file = request.POST.get('excel_file')
        print(excel_file)
        return render(request, self.template_name, context)

    template_name = 'import/step3.html'


class ValidateExcel(DomainRequiredMixin, FormView):
    def post(self, request):
        excel_file = request.FILES['excel_file']
        uploaded_wb = load_workbook(filename = excel_file)
        uploaded_ws = uploaded_wb.get_sheet_by_name(_('data'))

        # check headers
        obj = Template.objects.get(id='clean-template')
        tfile = getattr(obj, __('file'))
        wb = load_workbook(filename = tfile)
        ws = wb.get_sheet_by_name(_('data'))

        # FIXME: There shouldn't be two rows of headers
        header_row = 2
        for cell in uploaded_ws[header_row]:
            if cell.value != ws[header_row][cell.col_idx-1].value:
                raise Exception('Headers are not the same as in template! {} != {}'.format(cell.value, ws[header_row][cell.col_idx-1].value))

        context = {}
        context['columns'] = uploaded_ws[header_row]
        uploaded_ws.delete_rows(0, amount=header_row)
        context['data'] = uploaded_ws

        return render(request, self.template_name, context)

    template_name = 'import/step2.html'


class DownloadTemplate(DomainRequiredMixin, View):
    def get(self, request):
        # get localized excel template
        obj = Template.objects.get(id='clean-template')
        tfile = getattr(obj, __('file'))
        tfilename = tfile.name

        wb = load_workbook(filename = tfile)
        create_catalog(wb, request)

        # response
        response = HttpResponse(content=save_virtual_workbook(wb), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % (basename(tfilename),)
        return response


class ValidateDupesDoc(DomainRequiredMixin, TemplateView):
    template_name = 'dupes_document.html'


class ValidateDupesName(DomainRequiredMixin, TemplateView):
    template_name = 'dupes_name.html'


class SubProjectTableView(DomainRequiredMixin, PagedFilteredTableView):
    model = SubProject
    table_class = SubProjectTable
    template_name = 'table.html'
    paginate_by = 50
    filter_class = SubProjectFilter
    formhelper_class = SubProjectFilterFormHelper


class ProjectTableView(DomainRequiredMixin, PagedFilteredTableView):
    model = Project
    table_class = ProjectTable
    template_name = 'table.html'
    paginate_by = 50
    filter_class = ProjectFilter
    formhelper_class = ProjectFilterFormHelper


class ContactTableView(DomainRequiredMixin, PagedFilteredTableView):
    model = Contact
    table_class = ContactTable
    template_name = 'table.html'
    paginate_by = 50
    filter_class = ContactFilter
    formhelper_class = ContactFilterFormHelper


class ProjectContactTableView(DomainRequiredMixin, ReportExportMixin, PagedFilteredTableView):
    model = ProjectContact
    table_class = ProjectContactTable
    template_name = 'table.html'
    paginate_by = 50
    filter_class = ProjectContactFilter
    formhelper_class = ProjectContactFilterFormHelper


class DashboardView(DomainRequiredMixin, TemplateView):
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
