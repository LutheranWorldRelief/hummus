from django.contrib import admin
from django.apps import apps


# based on https://hackernoon.com/automatically-register-all-models-in-django-admin-django-tips-481382cf75e5

class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        not_allowed = ['password', 'colors']
        self.list_display = [field.name for field in model._meta.fields if field.name not in not_allowed ]
        if 'name' in self.list_display:
            self.search_fields = ['name']
        if 'country' in self.list_display:
            self.list_filter = [('country', admin.RelatedOnlyFieldListFilter)]
        super(ListAdminMixin, self).__init__(model, admin_site)


models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
