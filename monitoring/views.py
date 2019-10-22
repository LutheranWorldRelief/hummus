"""
'monitoring' views, mostly invoked by urls.py
"""
import json
import time
import datetime
from os.path import basename
from django.conf import settings

from django.db.models import Count, Q, Value, F
from django.db.models.functions import Upper, Trim, Coalesce
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView
from django.views.decorators.csrf import csrf_exempt

from constance import config
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook

from .tables import (SubProjectTable, ProjectTable, ContactTable, ProjectContactTable,
                     PagedFilteredTableView, ReportExportMixin,
                     SubProjectFilter, SubProjectFilterFormHelper,
                     ProjectFilter, ProjectFilterFormHelper,
                     ProjectContactFilter, ProjectContactFilterFormHelper,
                     ContactFilter, ContactFilterFormHelper, )
from .models import (SubProject, Project, Contact, Template, Organization, ProjectContact,
                     Request, City)
from .common import (DomainRequiredMixin, MONTHS, get_localized_name as __,
                     RegexpReplace)
from .catalog import create_catalog
from .updates import update_contact, update_project_contact


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
        messages = []
        context = {}
        row = Request()
        row.meta = request.META
        row.body = request.body.decode('utf-8')
        body = json.loads(row.body)
        row_dict = {}
        project_name = body['form'].get('project')
        project = Project.objects.get(name=project_name)
        try:
            row_dict['name'] = body['form'].get('name', '')
            row_dict['first_name'] = body['form'].get('first_name', '')
            row_dict['last_name'] = body['form'].get('last_name', '')
            row_dict['name'] = body['form'].get('name', '')
            row_dict['sex'] = body['form'].get('sex', '')
            row_dict['country'] = body['form'].get('country', '')
            row_dict['education'] = body['form'].get('education', '')
            row_dict['document'] = body['form'].get('id', '')
            row_dict['source_id'] = 'commcare'
        except KeyError as e:
            print('KeyError in data forwarding : "%s"' % str(e))

        # try to find contact
        contact = Contact.objects.filter(document=row_dict['document'],
                                         first_name=row_dict['first_name'],
                                         last_name=row_dict['last_name']).first()

        # using MDC sometimes only 'name' is collected, try to find contact
        if not contact:
            contact = Contact.objects.filter(document=row_dict['document'],
                                             name=row_dict['name']).first()

        if not contact:
            print('Create contact: {} {} {}'.format(row_dict['name'],
                                                    row_dict['first_name'], row_dict['last_name']))
            contact = Contact()
            update_contact(request, contact, row_dict)
        else:
            print('Update contact: {} {} {}'.format(row_dict['name'],
                                                    row_dict['first_name'], row_dict['last_name']))
            update_contact(request, contact, row_dict)

        project_contact = ProjectContact.objects.filter(project__name=project_name,
                                                        contact=contact).first()
        if not project_contact:
            print('Create project contact: {} {}'.format(project.name, row_dict['name']))
            project_contact = ProjectContact()
            project_contact.contact = contact
            project_contact.project = project
            update_project_contact(request, project_contact, row_dict)
        else:
            print('Update project contact: {} {}'.format(project.name, row_dict['first_name']))
            update_project_contact(request, project_contact, row_dict)
        return render(request, self.template_name, context)


class ImportParticipants(DomainRequiredMixin, FormView):

    def validate_data(self, row):
        message = ''
        project = row[0].value
        org_implementing = row[1].value
        document = row[2].value
        first_name = row[3].value
        last_name = row[4].value
        if not project:
            message = 'Problem to import record #{}, project is missing.'.format(row[0].row)
            return message

        if not org_implementing:
            message = 'Problem to import record #{}, implementing organization is missing.' \
                .format(row[0].row)
            return message

        if not document:
            message = 'Problem to import record #{}, document is missing.'.format(row[0].row)
            return message

        if not first_name:
            message = 'Problem to import record #{}, name is missing.'.format(row[0].row)
            return message

        if not last_name:
            message = 'Problem to import record #{}, lastname is missing.'.format(row[0].row)
            return message

        return message

    def post(self, request, *args, **kwargs):
        messages = []
        imported_ids = []

        tmp_excel = request.POST.get('excel_file')
        start_row = int(request.POST.get('start_row', config.START_ROW))
        date_format = request.POST.get('date_format', settings.SHORT_DATE_FORMAT)
        excel_file = default_storage.open('{}/{}'.format('tmp', tmp_excel))
        uploaded_wb = load_workbook(excel_file)
        uploaded_ws = uploaded_wb[_('data')]

        # creating the correct format date for python
        date_format = '%{}'.format(date_format.replace('/', '/%'))

        if date_format not in settings.ALLOWED_DATE_FORMATS:
            raise Exception('The Date format is incorrect!')

        # import
        project_cols = 2
        uploaded_ws.delete_rows(0, amount=start_row - 1)
        for row in uploaded_ws.iter_rows():
            error_message = self.validate_data(row)

            if error_message == '':
                # get SubProject, validates project columns
                project_name = row[0].value
                organization_name = row[1].value
                subproject = SubProject.objects.filter(project__name=project_name,
                                                       organization__name=organization_name).first()

                org_implementing = Organization.objects.filter(name=organization_name).first()
                if not subproject:
                    messages.append('Problem to import record #{} : '
                                    'Subproject with Project "{}" and Organization "{}"\
                        does not exist!'.format(row[0].row, project_name, organization_name))

                birthdate = row[project_cols + 4].value
                project_entry_date = row[project_cols + 13].value
                if birthdate:
                    birthdate = datetime.datetime.strptime(birthdate, date_format)
                else:
                    birthdate = None

                if project_entry_date:
                    project_entry_date = datetime.datetime.strptime(project_entry_date, date_format)
                else:
                    project_entry_date = None

                row_dict = {}
                project = Project.objects.get(name=project_name)
                row_dict['org_implementing_id'] = org_implementing.id
                row_dict['document'] = row[project_cols + 0].value
                row_dict['first_name'] = row[project_cols + 1].value
                row_dict['last_name'] = row[project_cols + 2].value
                row_dict['sex'] = row[project_cols + 3].value
                row_dict['birthdate'] = birthdate
                row_dict['education'] = row[project_cols + 5].value
                row_dict['phone'] = row[project_cols + 6].value
                row_dict['men_home'] = row[project_cols + 7].value
                row_dict['women_home'] = row[project_cols + 8].value
                row_dict['organization'] = row[project_cols + 9].value
                row_dict['country'] = row[project_cols + 10].value
                row_dict['departament'] = row[project_cols + 11].value
                row_dict['community'] = row[project_cols + 12].value
                row_dict['project_entry_date'] = project_entry_date
                row_dict['product'] = row[project_cols + 14].value
                row_dict['area'] = row[project_cols + 15].value
                row_dict['dev_area'] = row[project_cols + 16].value
                row_dict['age_dev'] = row[project_cols + 17].value
                row_dict['productive_area'] = row[project_cols + 18].value
                row_dict['age_prod'] = row[project_cols + 19].value
                row_dict['yield'] = row[project_cols + 20].value
                row_dict['source_id'] = 'excel'
                contact = Contact.objects.filter(document=row_dict['document'],
                                                 first_name=row_dict['first_name'],
                                                 last_name=row_dict['last_name']).first()
                contact_organization = Organization.objects.filter(
                    name=row_dict['organization']).first()
                if not contact_organization and row_dict['organization']:
                    messages.append('Create organization: {}'.format(row_dict['organization']))
                    if row_dict['organization']:
                        contact_organization = Organization()
                        contact_organization.name = row_dict['organization']
                        contact_organization.created_user = request.user.username
                        contact_organization.save()

                if not contact:
                    messages.append('Create contact: {} {}'.format(row_dict['first_name'],
                                                                   row_dict['last_name']))
                    contact = Contact()
                    if contact_organization:
                        contact.organization = contact_organization
                    update_contact(request, contact, row_dict)
                else:
                    messages.append('Update contact: {} {}'.format(row_dict['first_name'],
                                                                   row_dict['last_name']))
                    update_contact(request, contact, row_dict)

                imported_ids.append(contact.id)

                project_contact = ProjectContact.objects.filter(project__name=project_name,
                                                                contact=contact).first()
                if not project_contact:
                    messages.append('Create project contact: {} {}'.format(project.name,
                                                                           row_dict['first_name']))
                    project_contact = ProjectContact()
                    project_contact.contact = contact
                    project_contact.project = project
                    update_project_contact(request, project_contact, row_dict)
                else:
                    messages.append('Update project contact: {} {}'.format(project.name,
                                                                           row_dict['first_name']))
                    update_project_contact(request, project_contact, row_dict)
            else:
                messages.append(error_message)

        # gets dupes
        qs = Contact.objects.annotate(name_uc=Trim(Upper(RegexpReplace(F('name'),
                                                                       r'\s+', ' ', 'g'))))
        queryset1 = qs.values('name_uc').order_by('name_uc').annotate(cuenta=Count(
            'name_uc')).filter(cuenta__gt=1)
        names_uc = [row['name_uc'] for row in queryset1]
        contacts_names_ids = qs.values_list('id', flat=True).filter(name_uc__in=names_uc)

        queryset2 = Contact.objects.filter(document__isnull=False) \
            .exclude(document='').values('document') \
            .order_by('document') \
            .annotate(cuenta=Count('document')) \
            .filter(cuenta__gt=1)
        documents = [row['document'] for row in queryset2]

        contacts = Contact.objects.filter(id__in=imported_ids) \
            .filter(Q(id__in=contacts_names_ids) | Q(document__in=documents)) \
            .values(contact_id=F('id'),
                    contact_name=Coalesce('name', Value('')),
                    contact_sex=Coalesce('sex_id', Value('')),
                    contact_document=Coalesce('document', Value('')),
                    contact_organization=Coalesce('organization__name', Value('')),
                    )

        context = {}
        context['excel_file'] = tmp_excel
        context['messages'] = messages
        context['model'] = list(contacts)
        return render(request, self.template_name, context)

    template_name = 'import/step3.html'


class ValidateExcel(DomainRequiredMixin, FormView):
    def post(self, request, *args, **kwargs):
        # get advanced options
        language = request.POST.get('language', settings.LANGUAGE_CODE)
        start_row = int(request.POST.get('start_row', config.START_ROW))
        header_row = int(request.POST.get('header_row', config.HEADER_ROW))
        template = request.POST.get('template', config.DEFAULT_TEMPLATE)
        date_format = request.POST.get('date_format', settings.SHORT_DATE_FORMAT)

        # get file and set name
        excel_file = request.FILES['excel_file']
        tmp_excel_name = "{}-{}-{}".format(request.user.username, time.strftime("%Y%m%d-%H%M%S"),
                                           excel_file.name)
        default_storage.save('tmp/{}'.format(tmp_excel_name), excel_file)
        uploaded_wb = load_workbook(filename=excel_file)

        # gets the data sheet, tries all languages
        uploaded_ws = None
        if _('data') in uploaded_wb.sheetnames:
            uploaded_ws = uploaded_wb[_('data')]
        else:
            for other_lang in [lang[0] for lang in settings.LANGUAGES]:
                with translation.override(other_lang):
                    if _('data') in uploaded_wb.sheetnames:
                        uploaded_ws = uploaded_wb[_('data')]
                        continue
        if not uploaded_ws:
            uploaded_ws = uploaded_wb.active

        # check headers
        template_obj = Template.objects.get(id=template)
        mapping = getattr(template_obj, __('mapping', language))
        headers = [cell.value for cell in uploaded_ws[header_row]]

        # checks columns from mapping exist in uploaded file
        for model in mapping:
            for field in mapping[model]:
                column_name = mapping[model][field]['name']
                if column_name not in headers:
                    raise Exception('Column "{}" not found, choices are: {}'
                                    .format(column_name, ', '.join(filter(None, headers))))

        context = {}
        context['columns'] = uploaded_ws[header_row]
        uploaded_ws.delete_rows(0, amount=header_row)
        context['data'] = uploaded_ws
        context['start_row'] = start_row
        context['date_format'] = date_format
        context['excel_file'] = tmp_excel_name

        return render(request, self.template_name, context)

    template_name = 'import/step2.html'


class DownloadTemplate(DomainRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # get localized excel template
        obj = Template.objects.get(id=config.DEFAULT_TEMPLATE)
        tfile = getattr(obj, __('file'))
        tfilename = tfile.name

        book = load_workbook(filename=tfile)
        create_catalog(book, request)

        # response
        response = HttpResponse(content=save_virtual_workbook(book),
                                content_type='application/vnd.openxmlformats-officedocument.'
                                             'spreadsheetml.sheet')
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


class CityDetailView(DetailView):
    model = City

    def get_object(self, queryset=None):
        name = self.kwargs.get('name')
        country_id = self.kwargs.get('country_id')
        obj = City.objects.all()
        if country_id:
            obj = obj.filter(Q(country_id=country_id.upper()) | Q(country__name__iexact=country_id))
        obj = obj.filter(name__iexact=name).first()
        return obj
