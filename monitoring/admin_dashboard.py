"""
Custom Dashboard configuration for JET admin interface
"""
from django.utils.translation import ugettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard


class CustomIndexDashboard(Dashboard):
    columns = 3

    def init_with_context(self, context):
        self.children.append(modules.AppList(
            _('List Applications'),
            exclude=('auth.*', 'legacy.*', 'microsoft_auth.*', 'jet.*', 'contenttypes.*',
                     'sessions.*', 'sites.*', 'databse.*', 'constance.*', 'admin.*', 'database.*'),
            column=0,
            order=0
        ))

        self.available_children.append(modules.LinkList)
        self.children.append(modules.LinkList(
            _('Supporting'),
            children=[
                {
                    'title': _('Django documentation'),
                    'url': 'http://docs.djangoproject.com/',
                    'external': True,
                },
                {
                    'title': _('Django "django-users" mailing list'),
                    'url': 'http://groups.google.com/group/django-users',
                    'external': True,
                },
            ],
            column=0,
            order=0
        ))
        self.children.append(modules.RecentActions(
            _('Recent Actions'),
            10,
            column=1,
            order=0
        ))
