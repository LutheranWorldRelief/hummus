"""
updates and saves models. used by importers.
"""

from django.db.models import Q

from .common import get_localized_name as __
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

    project_contact.save()
