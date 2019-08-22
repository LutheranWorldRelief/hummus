from django.contrib import admin
from django.apps import apps
from import_export.admin import ImportExportModelAdmin
from .models import *

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


class ProjectContactInline(admin.StackedInline):
    model = ProjectContact
    extra = 0

class AttendanceInline(admin.StackedInline):
    model = Attendance
    extra = 0

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
    inlines = [
        ProjectContactInline,
        AttendanceInline,
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
    date_hierarchy = 'start'
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


class EventInline(admin.TabularInline):
    model = Event
    extra = 0


class StructureInline(admin.TabularInline):
    model = Structure
    extra = 0


class ProjectAdmin(admin.ModelAdmin):
    inlines = [
        StructureInline,
    ]
    list_display = (
        'code', 'name', 'get_countries', 'goalmen', 'goalwomen', 'get_women', 'get_men', 'get_total')
    list_per_page = 20
    list_max_show_all = 50
    list_display_links = ['name']
    ordering = ['id']
    search_fields = ['code', 'name', ]
    date_hierarchy = 'start'
    fieldsets = [
        ('General information',{'fields': ['id','code','name','logo','colors','url']}),
        ('Date information', {'fields': ['start', 'end']}),
        ('Goal', {'fields': ['goalmen', 'goalwomen']}),
    ]

    def get_countries(self, obj):
        return ', '.join(
            Event.objects.filter(structure__project_id=obj.id).order_by('country').values_list('country__name',
                                                                                               flat=True).distinct())

    get_countries.short_description = 'Countries'

    def get_women(self, obj):
        return 0

    get_women.short_description = 'M'

    def get_men(self, obj):
        return 0

    get_men.short_description = 'H'

    def get_total(self, obj):
        return self.get_men(obj) + self.get_women(obj)

    get_total.short_description = 'T'


class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
    'id', 'name', 'description', 'country', 'organization_parent', 'organization_type', 'is_implementer')
    list_per_page = 20
    list_max_show_all = 50
    ordering = ['id']
    list_filter = [
    ('name', DropdownFilter),
    ('country', RelatedOnlyDropdownFilter),
   ('organization_type', RelatedOnlyDropdownFilter),
    ]
    search_fields = ['id', 'name', 'description', 'country__name']
    autocomplete_fields = ('country', 'organization_type',)
    exclude = ['id']

    def organization_parent(self, object):
        if object.organization_id is not None:
            return object.name
        else:
            return ''

 
class StructureAdmin(ListAdminMixin, ImportExportModelAdmin):
    inlines = [
        EventInline,
    ]

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'contact', 'type', 'country','organization')
    list_display_links = ['id', 'event']
    list_per_page = 20
    list_max_show_all = 50
    ordering = ['event']
    list_filter = [
        ('country', RelatedOnlyDropdownFilter),
        ('organization__name', DropdownFilter),
        'type'
    ]
    search_fields = ['contact__name', 'event__name']

    def project_name(self, obj):
        if obj.projectcontact:
            return obj.projectcontact.project
        else:
            return ''


admin.site.register(Structure, StructureAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Attendance, AttendanceAdmin)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, ImportExportModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
