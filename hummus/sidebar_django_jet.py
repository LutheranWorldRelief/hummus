from django.utils.translation import gettext_lazy as _


def get_django_jet_menu():
    return [
        {'label': _('Import Participants'), 'permissions': ['monitoring.add_projectcontact',
                                                            'monitoring.change_projectcontact',
                                                            'monitoring.add_contact',
                                                            'monitoring.change_contact'], 'items': [
            {'name': '', 'url': '/import/participants/step1  ',
             'label': _('Import Participants')},
        ]},
        {'label': _('Participants'), 'permissions': ['monitoring.view_contact'], 'items': [
            {'name': 'monitoring.contact', 'label': _('Participants'),
             'permissions': ['monitoring.view_contact']},
            {'name': '', 'url': '/validate/dupes-name', 'label': _('Duplicates by Name'),
             'permissions': ['monitoring.change_contact', 'monitoring.change_projectcontact']},
            {'name': '', 'url': '/validate/dupes-doc', 'label': _('Duplicates per document'),
             'permissions': ['monitoring.change_contact', 'monitoring.change_projectcontact']},
        ]},
        {'label': _('Reports'), 'permissions': ['monitoring.view_projectcontact',
                                                'monitoring.view_country',
                                                'monitoring.view_contact',
                                                'monitoring.view_organization'], 'items': [
            {'name': '', 'url': '/export/participants', 'label': _('Project Participants')},
            {'name': '', 'url': '/export/template-clean/', 'label': _('Clean Template'),
             'permissions': ['monitoring.add_projectcontact',
                             'monitoring.change_projectcontact',
                             'monitoring.add_contact',
                             'monitoring.change_contact']},
        ]},
        {'label': _('Dashboard'), 'items': [
            {'name': '', 'url': '/dashboard/', 'label': _('Dashboard')},
        ]},
        {'label': _('Data Tables'), 'items': [
            {'name': 'monitoring.project', 'label': _('Projects'), 'permissions': [
                'monitoring.view_project']},
            {'name': 'monitoring.organization', 'label': _('Organizations'),
             'permissions': ['monitoring.view_organization']},
            {'name': 'monitoring.organizationtype', 'label': _('Types'),
             'permissions': ['monitoring.view_organizationtype']},
            {'name': 'monitoring.country', 'label': _('Countries'), 'permissions': [
                'monitoring.view_country']},
            {'name': 'monitoring.contacttype', 'label': _('Contact Types'), 'permissions': [
                'monitoring.view_contacttype']},
            {'name': 'monitoring.education', 'label': _('Educations'), 'permissions': [
                'monitoring.view_education']},
            {'name': 'monitoring.sex', 'label': _('Sex'), 'permissions': ['monitoring.view_sex']},
            {'name': 'monitoring.lwrregion', 'label': _('Regions'), 'permissions': [
                'monitoring.view_lwrregion']},
            {'name': 'monitoring.filter', 'label': _('Segmentation'), 'permissions': [
                'monitoring.view_filter']},
        ]},
        {'label': _('Security'), 'permissions': ['request.user.is_superuser'], 'items': [
            {'name': 'auth.user', 'label': _('Users')},
            {'name': 'auth.group', 'label': _('Roles')},
            {'name': 'monitoring.profile', 'label': _('Profiles')},
        ]}
    ]
