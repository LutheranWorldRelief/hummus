"""
'monitoring' views, mostly invoked by urls.py
"""
import time
from os.path import basename

from django.db.models import Count, Q, Value, F
from django.db.models.functions import Upper, Trim, Coalesce
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView
from django.views.decorators.csrf import csrf_exempt

from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook

from .tables import (SubProjectTable, ProjectTable, ContactTable, ProjectContactTable,
                     PagedFilteredTableView, ReportExportMixin,
                     SubProjectFilter, SubProjectFilterFormHelper,
                     ProjectFilter, ProjectFilterFormHelper,
                     ProjectContactFilter, ProjectContactFilterFormHelper,
                     ContactFilter, ContactFilterFormHelper,)
from .models import SubProject, Project, Contact, Template, Organization, ProjectContact, Request
from .common import (DomainRequiredMixin, MONTHS, get_localized_name as __,
                     RegexpReplace)
from .catalog import create_catalog


@method_decorator(csrf_exempt, name='dispatch')
class Capture(TemplateView):
    template_name = 'capture.html'

    # TODO: GET should be removed
    def get(self, request, *args, **kwargs):
        context = {}
        context['meta'] = request.META
        context['body'] = request.body.decode('utf-8')
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = {}
        row = Request()
        row.meta = request.META
        row.body = request.body.decode('utf-8')
        row.created_user = request.user.username
        row.save()
        return render(request, self.template_name, context)


class ImportParticipants(DomainRequiredMixin, FormView):

    def update_contact(self, request, contact, row):
        first_name = row['first_name'].strip()
        last_name = row['last_name'].strip()
        name = "{} {}".format(first_name, last_name)
        contact.first_name = first_name
        contact.last_name = last_name
        contact.name = name
        contact.document = row['document']
        if contact.id:
            contact.updated_user = request.user.username
        else:
            contact.created_user = request.user.username
        # TODO : complete fields
        contact.save()

    def update_project_contact(self, request, project_contact, row):
        if project_contact.id:
            project_contact.updated_user = request.user.username
        else:
            project_contact.created_user = request.user.username
        # TODO : complete fields
        project_contact.save()

    def post(self, request, *args, **kwargs):

        messages = []
        imported_ids = []

        tmp_excel = request.POST.get('excel_file')
        excel_file = default_storage.open('{}/{}'.format('tmp', tmp_excel))
        uploaded_wb = load_workbook(excel_file)
        uploaded_ws = uploaded_wb[_('data')]

        # import
        header_rows = 2
        project_cols = 2
        uploaded_ws.delete_rows(0, amount=header_rows)
        for row in uploaded_ws.iter_rows():

            # get SubProject, validates project columns
            project_name = row[0].value
            organization_name = row[1].value
            subproject = SubProject.objects.filter(project__name=project_name,
                                                   organization__name=organization_name).first()
            if not subproject:
                raise Exception('Row # {} : Subproject with Project "{}" and Organization "{}"\
                    does not exist!'.format(row[0].row, project_name, organization_name))

            row_dict = {}
            project = Project.objects.get(name=project_name)
            row_dict['document'] = row[project_cols + 0].value
            row_dict['first_name'] = row[project_cols + 1].value
            row_dict['last_name'] = row[project_cols + 2].value
            row_dict['sex'] = row[project_cols + 3].value
            row_dict['birthdate'] = row[project_cols + 4].value
            row_dict['education'] = row[project_cols + 5].value
            row_dict['phone'] = row[project_cols + 6].value
            row_dict['men_home'] = row[project_cols + 7].value
            row_dict['women_home'] = row[project_cols + 8].value
            row_dict['organization'] = row[project_cols + 9].value
            row_dict['country'] = row[project_cols + 10].value
            contact = Contact.objects.filter(document=row_dict['document'],
                                             first_name=row_dict['first_name'],
                                             last_name=row_dict['last_name']).first()
            contact_organization = Organization.objects.filter(
                name=row_dict['organization']).first()
            if not contact_organization and row_dict['organization']:
                messages.append('Create organization: {}'.format(row_dict['organization']))
                if row_dict['organization']:
                    contact_organization = Organization()
                    # TODO : complete fields
                    contact_organization.name = row_dict['organization']
                    contact_organization.created_user = request.user.username
                    contact_organization.save()

            if not contact:
                messages.append('Create contact: {} {}'.format(row_dict['first_name'],
                                                               row_dict['last_name']))
                contact = Contact()
                if contact_organization:
                    contact.organization = contact_organization
                self.update_contact(request, contact, row_dict)
            else:
                messages.append('Update contact: {} {}'.format(row_dict['first_name'],
                                                               row_dict['last_name']))
                self.update_contact(request, contact, row_dict)

            imported_ids.append(contact.id)

            project_contact = ProjectContact.objects.filter(project__name=project_name,
                                                            contact=contact).first()
            if not project_contact:
                messages.append('Create project contact: {} {}'.format(project.name,
                                                                       row_dict['first_name']))
                project_contact = ProjectContact()
                project_contact.contact = contact
                project_contact.project = project
                self.update_project_contact(request, project_contact, row_dict)
            else:
                messages.append('Update project contact: {} {}'.format(project.name,
                                                                       row_dict['first_name']))
                self.update_project_contact(request, project_contact, row_dict)

            # FOR REFERENCE:  enumerate(['Identification number', 'Name', 'Last name', 'Sex',
            # 'Birthdate', 'Education', 'Phone', 'Men in your family', 'Women in your family',
            # 'Organization belonging', 'Country Department', 'Community', 'Project entry date',
            # 'Item', 'Estate area (hectares)', 'Developing Area (hectares)', 'Planting Age in
            # Development (years)', 'Production Area (hectares)', 'Planting Age in Production
            # (years)', 'Yields (qq)']):

        # gets dupes
        qs = Contact.objects.annotate(name_uc=Trim(Upper(RegexpReplace(F('name'),
                                                                       r'\s+', ' ', 'g'))))
        queryset1 = qs.values('name_uc').order_by('name_uc').annotate(cuenta=Count(
            'name_uc')).filter(cuenta__gt=1)
        names_uc = [row['name_uc'] for row in queryset1]
        contacts_names_ids = qs.values_list('id', flat=True).filter(name_uc__in=names_uc)

        queryset2 = Contact.objects.filter(document__isnull=False).exclude(
            document='').values('document').order_by(
                'document').annotate(cuenta=Count('document')).filter(cuenta__gt=1)
        documents = [row['document'] for row in queryset2]

        contacts = Contact.objects.filter(id__in=imported_ids) \
            .filter(
                Q(id__in=contacts_names_ids) | Q(document__in=documents)).values(
                    contact_id=F('id'),
                    contact_name=Coalesce('name', Value('')),
                    contact_sex=Coalesce('sex_id', Value('')),
                    contact_document=Coalesce('document', Value('')),
                    contact_organization=Coalesce('organization__name', Value('')),
        )

        # contacts = list(contacts)

        context = {}
        context['excel_file'] = tmp_excel
        context['messages'] = messages
        context['model'] = list(contacts)
        return render(request, self.template_name, context)

    template_name = 'import/step3.html'


class ValidateExcel(DomainRequiredMixin, FormView):
    def post(self, request, *args, **kwargs):
        excel_file = request.FILES['excel_file']
        tmp_excel_name = "{}-{}-{}".format(request.user.username, time.strftime("%Y%m%d-%H%M%S"),
                                           excel_file.name)
        uploaded_wb = load_workbook(filename=excel_file)
        uploaded_ws = uploaded_wb[_('data')]

        # check headers
        obj = Template.objects.get(id='clean-template')
        tfile = getattr(obj, __('file'))
        book = load_workbook(filename=tfile)
        sheet = book[_('data')]

        # FIXME: There shouldn't be two rows of headers
        header_row = 2
        for cell in uploaded_ws[header_row]:
            if cell.value != sheet[header_row][cell.col_idx - 1].value:
                raise Exception('Headers are not the same as in template! {} != {}'.format(
                    cell.value, sheet[header_row][cell.col_idx - 1].value))

        context = {}
        context['columns'] = uploaded_ws[header_row]
        uploaded_ws.delete_rows(0, amount=header_row)
        context['data'] = uploaded_ws
        context['excel_file'] = tmp_excel_name

        return render(request, self.template_name, context)

    template_name = 'import/step2.html'


class DownloadTemplate(DomainRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # get localized excel template
        obj = Template.objects.get(id='clean-template')
        tfile = getattr(obj, __('file'))
        tfilename = tfile.name

        book = load_workbook(filename=tfile)
        create_catalog(book, request)

        # response
        response = HttpResponse(content=save_virtual_workbook(book),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                                )
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['months'] = MONTHS
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
