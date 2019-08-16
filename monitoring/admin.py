from django.contrib import admin
from django.apps import apps
from import_export.admin import ImportExportModelAdmin
from .models import Contact, Event, Project, ProjectContact

from django_admin_listfilter_dropdown.filters import (
    DropdownFilter, RelatedOnlyDropdownFilter
)


# based on https://hackernoon.com/automatically-register-all-models-in-django-admin-django-tips-481382cf75e5

class ListAdminMixin(object):
    def __init__(self, model, admin_site):
        not_allowed = ['password', 'colors']
        self.list_filter = []
        self.list_display = [field.name for field in model._meta.fields if field.name not in not_allowed]
        if 'name' in self.list_display:
            self.search_fields = ['name']
        if 'type' in self.list_display:
            self.list_filter.append(('type', admin.RelatedOnlyFieldListFilter))
        if 'country' in self.list_display:
            self.list_filter.append(('country', admin.RelatedOnlyFieldListFilter))
        super(ListAdminMixin, self).__init__(model, admin_site)


class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'document', 'country', 'organization', 'type', 'title')
    list_display_links = ['name', 'country', 'type']
    list_per_page = 20
    list_max_show_all = 50
    ordering = ['name']
    list_filter = [
        ('country', RelatedOnlyDropdownFilter),
        ('organization__name', DropdownFilter),
        'type'
    ]
    search_fields = ['name', 'country__name', 'document', 'organization__name', 'title']
    autocomplete_fields = ('country', 'organization', 'type', 'education')


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project_name', 'structure', 'country', 'organization', 'start',
                    'men', 'women', 'total')
    list_display_links = ['name']
    list_per_page = 20
    list_max_show_all = 50
    ordering = ['-start']
    list_filter = [
        ('country', RelatedOnlyDropdownFilter),
        ('organization', RelatedOnlyDropdownFilter),
    ]
    search_fields = ['id', 'name', 'project__name', 'structure__name', 'organization__name', 'country__name']

    def project_name(self, obj):
        if obj.structure:
            return obj.structure.project
        else:
            return ''

    def men(self, obj):
        return obj.attendance_set.filter(contact__sex='M').count()

    def women(self, obj):
        return obj.attendance_set.filter(contact__sex='F').count()

    def total(self, obj):
        return self.men(obj) + self.women(obj)

    class Media:
        css = {
            'all': ('css/table_event.css',)
        }


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'countries', 'goal__men', 'goal__women','woman')
    list_per_page = 20
    list_max_show_all = 50
    list_display_links = ['name']
    ordering = ['id']

    def countries(self, obj):
        return ', '.join(
            Event.objects.filter(structure__project_id=obj.id).order_by('country').values_list('country__name',
                                                                                               flat=True).distinct())

    def goal__men(self, obj):
        if obj.goal_men is not None:
            return obj.goal_men
        else:
            return 0

    def goal__women(self, obj):
        if obj.goal_women is not None:
            return obj.goal_women
        else:
            return 0

    def woman(self, obj):
        a = ProjectContact.contact.filter(sex='F')
        print(a)
        # print(obj.projectcontact_set.contact)
        # return ProjectContact.objects.filter(project__id=obj.id).count()
        # count = Event.objects.filter(structure__project_id=obj.id).values_list('attendance__contact').filter(sex='F').count()
        # return count


admin.site.register(Contact, ContactAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Project, ProjectAdmin)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, ImportExportModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
