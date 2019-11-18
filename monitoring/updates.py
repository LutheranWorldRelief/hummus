"""
updates and saves models. used by importers.
"""

from django.apps import apps
from django.core.cache import cache
from django.db.models import Q
from django.utils.text import slugify

from .common import get_localized_name as __, parse_date, smart_assign, xstr
from .models import Sex, Education, Country, Organization


def try_to_find(model, value, exists=False):
    """ tries to find value in model """

    if not value:
        return None

    if isinstance(value, str):
        value = xstr(value)

    cache_key = "{}.{}.{}".format(model._meta.model_name, slugify(value), exists)
    found = cache.get(cache_key)
    if not found:
        filter_type = 'iexact'  # be case insensitive
        fields = ['name', 'varname']
        condition = Q(pk=None)  # start with always false

        for field in fields.copy():
            fields.append(__(field))

        for field in fields:
            field_filter = '{}__{}'.format(field, filter_type)
            if hasattr(model, field):
                condition = (condition | Q(**{field_filter: value}))

        if exists:
            found = model.objects.filter(condition).exists()
        else:
            found = model.objects.filter(condition).first()
    cache.set(cache_key, found)
    return found


def update_contact(request, contact, row):
    if request:
        if contact.id:
            contact.updated_user = request.user.username
        else:
            contact.created_user = request.user.username

    contact.name = smart_assign(contact.name, row.get('name'))
    contact.first_name = smart_assign(contact.first_name, row.get('first_name'))
    contact.last_name = smart_assign(contact.last_name, row.get('last_name'))
    contact.source_id = smart_assign(contact.source_id, row.get('source_id'))
    contact.document = smart_assign(contact.document, row.get('document'))
    contact.phone_personal = smart_assign(contact.phone_personal, row.get('phone_personal'))
    contact.women_home = smart_assign(contact.women_home, row.get('women_home'))
    contact.men_home = smart_assign(contact.men_home, row.get('men_home'))
    contact.birthdate = smart_assign(contact.birthdate, row.get('birthdate'))
    contact.municipality = smart_assign(contact.municipality, row.get('municipality'))
    contact.community = smart_assign(contact.community, row.get('community'))
    contact.location = smart_assign(contact.location, row.get('location'))
    contact.log = smart_assign(contact.log, row.get('log'))

    organization = try_to_find(Organization, row.get('organization'))
    sex = try_to_find(Sex, row.get('sex'))
    education = try_to_find(Education, row.get('education'))
    country = try_to_find(Country, row.get('country'))

    contact.organization_id = organization.id if organization else contact.organization_id
    contact.sex_id = sex.id if sex else contact.sex_id
    contact.education_id = education.id if education else contact.education_id
    contact.country_id = country.id if country else contact.country_id

    contact.save()


def update_project_contact(request, project_contact, row):
    if project_contact.id:
        project_contact.updated_user = request.user.username
    else:
        project_contact.created_user = request.user.username

    project_contact.organization = row.get('organization')
    project_contact.date_entry_project = smart_assign(project_contact.date_entry_project,
                                                      row.get('date_entry_project'))
    project_contact.source_id = row.get('source_id')
    project_contact.log = row.get('log')

    project_contact.save()


def validate_data(row, mapping, start_row=0, date_format=None):
    """ validates an excel row """
    messages = []
    app_name = 'monitoring'
    map_models = {'project': 'SubProject', 'contact': 'Contact',
                  'project_contact': 'ProjectContact'}
    offset = start_row - 1
    filter_type = 'iexact'

    for model_name in mapping:
        model = apps.get_model(app_name, map_models[model_name])

        # validate subproject = project + impleementer
        if model_name == 'project':
            subproject = model.objects.all()
            model_fields = mapping['project']
            for field_name, field_data in model_fields.items():
                value = row[field_data['column']].value
                if value and field_name == 'name' and '=>' in value:
                    code, value = value.split('=>', 2)
                if field_name == 'name' and not subproject.filter(name__iexact=value).exists():
                    field_name = 'project'
                if model._meta.get_field(field_name).get_internal_type() == 'ForeignKey':
                    field_name = "{}__name".format(field_name)
                field_name = '{}__{}'.format(field_name, filter_type)
                subproject = subproject.filter(**{field_name: value})
            if not subproject:
                project = row[model_fields['name']['column']].value
                organization = row[model_fields['organization']['column']].value
                messages.append('[{}]: Subproject with Project "{}" and Organization "{}" '
                                'does not exist!'.format(row[0].row + offset,
                                                         project,
                                                         organization, ))

        for field, details in mapping[model_name].items():
            cell = row[details['column']]
            try:
                reference = "{}{}".format(cell.column_letter, cell.row + offset)
            except AttributeError:
                # tolarates merged cells
                reference = "{}".format(cell.row + offset)
            value = cell.value

            # validates required fields
            if details['required'] and not value:
                messages.append('[{}]: {} is required'.format(reference, details['name']))

            if model_name == 'project' and field == 'name':
                field = 'project'
                if value and '=>' in value:
                    code, value = value.split('=>', 2)

            if value and hasattr(model, field):

                # validates date feilds
                if model._meta.get_field(field).get_internal_type() == 'DateField':
                    if not cell.is_date and not parse_date(value, date_format):
                        messages.append('[{}]: {} "{}" is not a valid date. Use {}.'.
                                        format(reference, field, value, date_format))

                # validates foreign keys
                if model._meta.get_field(field).get_internal_type() == 'ForeignKey':
                    related_model = model._meta.get_field(field).related_model
                    found = try_to_find(related_model, value, exists=True)
                    # TODO exception should be mapped like: "autoadd: True"
                    is_exception = model_name == 'contact' and field == 'organization'
                    if not found and not is_exception:
                        if related_model.objects.count() <= 10:
                            options = list(related_model.objects.values_list('name', flat=True))
                            options_trans = list(related_model.objects.values_list(__('name'),
                                                                                   flat=True))
                            options.extend(options_trans)
                            messages.append('[{}]: "{}" not found in {}. Options are {}'.
                                            format(reference, value, field, options))
                        else:
                            messages.append('[{}]: "{}" not found in {}.'.
                                            format(reference, value, field))
    if not messages:
        return None
    return {'row': 'Row #{}'.format(row[0].row + offset), 'msgs': messages}
