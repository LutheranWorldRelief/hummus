"""
updates and saves models. used by importers.
"""

from django.db.models import Q

from .common import get_localized_name as __
from .models import Sex, Education, Country, Product


def update_contact(request, contact, row):
    columna_name = __('name')
    columna_varname = __('varname')
    first_name = row['first_name'].strip()
    last_name = row['last_name'].strip()
    name = "{} {}".format(first_name, last_name)
    contact.first_name = first_name
    contact.last_name = last_name
    contact.name = name
    contact.source_id = row.get('source_id')
    contact.document = row.get('document', '').strip()
    contact.women_home = row.get('women_home')
    contact.men_home = row.get('men_home')
    contact.municipality = row.get('departament', '').strip()
    contact.community = row.get('community', '').strip()

    if contact.id:
        contact.updated_user = request.user.username
    else:
        contact.created_user = request.user.username

    sex = Sex.objects.filter(Q(**{columna_name: row['sex']}) |
                             Q(**{columna_varname: row['sex']})).first()
    education = Education.objects.filter(Q(**{columna_name: row['education']}) |
                                         Q(**{columna_varname: row['education']})).first()
    country = Country.objects.filter(**{columna_name: row['country']}).first()

    contact.sex_id = sex.id if sex else 'N'
    contact.education_id = education.id if education else None
    contact.country_id = country.id if country else None

    contact.save()


def update_project_contact(request, project_contact, row):
    columna_name = __('name')
    if project_contact.id:
        project_contact.updated_user = request.user.username
    else:
        project_contact.created_user = request.user.username

    project_contact.organization_id = row['org_implementing_id']

    product = Product.objects.filter(**{columna_name: row['product']}).first()

    project_contact.product_id = product.id if product else None
    project_contact.area = row['area'] if row['area'] else None
    project_contact.development_area = row['dev_area'] if row['dev_area'] else None
    project_contact.age_development_plantation = row['age_dev'] if row['age_dev'] else None
    project_contact.productive_area = row['productive_area'] if row['productive_area'] else None
    project_contact.age_productive_plantation = row['age_prod'] if row['age_prod'] else None
    project_contact.yield_field = row['yield'] if row['yield'] else None

    project_contact.save()
