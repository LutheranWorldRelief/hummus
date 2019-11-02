"""
updates and saves models. used by importers.
"""

from django.db.models import Q
from django.apps import apps

from .common import get_localized_name as __, parse_date
from .models import Sex, Education, Country, Product


def update_contact(request, contact, row):
    if request:
        if contact.id:
            contact.updated_user = request.user.username
        else:
            contact.created_user = request.user.username

    columna_name = __('name')
    columna_varname = __('varname')

    contact.name = row.get('name', '')
    contact.first_name = row.get('first_name')
    contact.last_name = row.get('last_name')
    contact.source_id = row.get('source_id')
    contact.document = row.get('document')
    contact.phone_personal = row.get('phone_personal')
    contact.women_home = row.get('women_home')
    contact.men_home = row.get('men_home')
    contact.birthdate = row.get('birthdate')
    contact.municipality = row.get('municipality')
    contact.community = row.get('community')
    contact.location = row.get('location')
    contact.log = row.get('log')

    sex = row.get('sex')
    if sex:
        sex = Sex.objects.filter(Q(**{columna_name: sex}) |
                                 Q(**{columna_varname: sex})).first()
    education = row.get('education')
    if education:
        education = Education.objects.filter(Q(**{columna_name: education}) |
                                             Q(**{columna_varname: education})).first()
    country = row.get('country')
    if country:
        country = Country.objects.filter(**{columna_name: country}).first()

    contact.sex_id = sex.id if sex else None
    contact.education_id = education.id if education else None
    contact.country_id = country.id if country else None

    contact.save()


def update_project_contact(request, project_contact, row):
    if project_contact.id:
        project_contact.updated_user = request.user.username
    else:
        project_contact.created_user = request.user.username

    project_contact.organization = row.get('organization')
    project_contact.date_entry_project = row.get('date_entry_project')
    project_contact.source_id = row.get('source_id')
    project_contact.log = row.get('log')

    project_contact.save()


def try_to_find(model, value):
    """ tries to find value in model """

    if not value:
        return

    filter_type = 'iexact'
    fields = ['name', 'varname']
    condition = Q(pk=None) # start with always false

    for field in fields.copy():
        fields.append(__(field))

    for field in fields:
        field_filter = '{}__{}'.format(field, filter_type)
        if hasattr(model, field):
            condition = (condition | Q(**{field_filter: value}))

    return model.objects.filter(condition)


def validate_data(row, mapping, start_row=0, date_format=None):
    """ validates an excel row """
    messages = []
    app_name = 'monitoring'
    map_models = {'project': 'SubProject', 'contact': 'Contact',
                  'project_contact': 'ProjectContact'}
    offset = start_row - 1

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
                if field_name == 'name' and not subproject.filter(name=value).exists():
                    field_name = 'project'
                if model._meta.get_field(field_name).get_internal_type() == 'ForeignKey':
                    field_name = "{}__name".format(field_name)
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
                    found = try_to_find(related_model, value)
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
    error_message = []
    if messages:
        error_message.append({'row': 'Row #{}'.format(row[0].row + offset), 'msgs': messages})
    return error_message
