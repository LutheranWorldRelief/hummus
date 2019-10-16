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
            _('Quick Liks'),
            models=('monitoring.Project', 'monitoring.Organization',
                    'monitoring.Contact', 'monitoring.Profile',
                    'auth.User', 'auth.Group','auth.Permission',
                    'constance.Config','monitoring.ProjectContact'),
            column=0,
            order=0
        ))

        self.children.append(modules.AppList(
            _('Catalogs'),
            models=('monitoring.Sex', 'monitoring.Country',
                    'monitoring.OrganizationType', 'monitoring.LWRRegion',
                    'monitoring.Product', 'monitoring.Education',
                    'monitoring.ContactType'),
            column=1,
            order=0
        ))

        self.children.append(modules.AppList(
            _('Extras'),
            models=('monitoring.Request', 'monitoring.Template',
                    'monitoring.Source', 'monitoring.Filter'),
            column=2,
            order=0
        ))

        if context.request.user.is_superuser:
            self.children.append(modules.RecentActions(
                _('Recent Actions'),
                10,
                column=2,
                order=1
            ))
