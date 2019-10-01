from django.apps import apps
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from jet.admin import CompactInline
from import_export import resources
from import_export.admin import ImportExportModelAdmin

from .models import *


# Change default query
class AdminForUserMixin(object):
    def get_queryset(self, request):
        if request.user:
            return self.model.objects.for_user(request.user)
        else:
            return super().get_queryset(request)


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


# Inlines Class
class ProjectContactInline(admin.TabularInline):
    model = ProjectContact
    fields = ('project',)
    readonly_fields = ('project',)
    show_change_link = True
    can_delete = False
    extra = 0

    def has_add_permission(self, request, **kwargs):
        return False


class CountryInline(CompactInline):
    model = Country
    can_delete = False
    extra = 0


class SubProjectsInline(CompactInline):
    model = SubProject
    can_delete = False
    extra = 0


# Admin Class
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'document', 'country', 'organization', 'type', 'title')
    list_display_links = ['name', 'country', 'type']
    list_per_page = 20
    list_max_show_all = 50
    ordering = ['name']
    list_filter = [
        ('country'),
        ('organization__name'),
        'type'
    ]
    inlines = [
        ProjectContactInline,
    ]
    search_fields = ['name', 'country__name', 'document', 'organization__name', 'title']


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'project_name', 'structure', 'country', 'organization', 'start',
                    'men', 'women', 'total')
    list_display_links = ['name']
    list_per_page = 20
    list_max_show_all = 50
    ordering = ['-start']
    date_hierarchy = 'start'
    list_filter = [
        ('country'),
        ('organization'),
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


class ProjectAdmin(AdminForUserMixin, admin.ModelAdmin):
    inlines = [
        SubProjectsInline,
    ]
    list_display = (
        'code', 'name', 'status', 'get_countries', 'lwrregion', 'targetmen', 'targetwomen', 'get_women', 'get_men',
        'get_total')
    list_per_page = 20
    list_max_show_all = 50
    list_display_links = ['name']
    ordering = ['id']
    search_fields = ['code', 'name', ]
    date_hierarchy = 'start'
    readonly_fields = ['show_salesforce_url']
    fieldsets = [
        (_('General information'),
         {'fields': ['code', 'name', 'status', 'logo', 'colors', 'url', 'lwrregion', 'show_salesforce_url']}),
        (_('Countries'), {'fields': ['countries']}),
        (_('Date information'), {'fields': ['start', 'end']}),
        (_('Goal'), {'fields': ['targetmen', 'targetwomen']}),
    ]

    list_filter = [
        ('status'),
        ('countries', admin.RelatedOnlyFieldListFilter),
        ('lwrregion'),
    ]

    def show_salesforce_url(self, obj):
        return format_html("<a a target='_blank' href='{url}'>{url}</a>", url=obj.salesforce_url)

    show_salesforce_url.short_description = "Salesforce Link"

    def get_countries(self, obj):
        return ', '.join([country.name for country in obj.countries.all()])

    get_countries.short_description = _('Countries')

    def get_women(self, obj):
        return 0

    get_women.short_description = _('Women')

    def get_men(self, obj):
        return 0

    get_men.short_description = _('Men')

    def get_total(self, obj):
        return self.get_men(obj) + self.get_women(obj)

    get_total.short_description = _('T')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description', 'country', 'organization_parent', 'organization_type', 'is_implementer')
    list_per_page = 20
    list_max_show_all = 50
    ordering = ['id']
    list_filter = [
        ('name'),
        ('country'),
        ('organization_type'),
    ]
    search_fields = ['id', 'name', 'description', 'country__name']
    exclude = ['id']

    def organization_parent(self, object):
        if object.organization_id is not None:
            return object.name
        else:
            return ''


class ProjectContactAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'project', 'contact', 'getCountryContact', 'product', 'area', 'date_entry_project', 'date_end_project',
        'yield_field')
    list_display_links = ['id', 'project']
    ordering = ['-date_entry_project']
    list_per_page = 20
    list_max_show_all = 50
    search_fields = ['id', 'project__name', 'contact__name', 'product__name']
    list_filter = [
        ('product'),
        ('contact__country', admin.RelatedOnlyFieldListFilter)
    ]

    def getCountryContact(self, obj):
        return obj.contact.country

    getCountryContact.short_description = 'Country'


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'language')
    list_display_links = ('id', 'user')
    ordering = ['-id']
    list_per_page = 20
    list_max_show_all = 50
    search_fields = ['id', 'user__username']
    list_filter = [
        ('language')
    ]


class SubprojectAdmin(AdminForUserMixin, admin.ModelAdmin):
    list_display = ('name', 'code', 'project', 'organization')
    list_display_links = ('name',)
    ordering = ['project']
    list_per_page = 20
    list_max_show_all = 50
    readonly_fields = ['show_salesforce_url']
    search_fields = ['name', 'code', 'project__name', 'status']
    fieldsets = [
        (_('General information'), {'fields': ['code', 'name', 'project', 'status', 'country', 'show_salesforce_url']}),
        (_('Date information'), {'fields': ['start', 'end']}),
        (_('Goals'), {'fields': ['targetimen', 'targetiwomen', 'targetmen', 'targetwomen']}),
    ]
    list_filter = [
        ('status'),
        ('country', admin.RelatedOnlyFieldListFilter),
        ('project__lwrregion'),
    ]

    def show_salesforce_url(self, obj):
        return format_html("<a a target='_blank' href='{url}'>{url}</a>", url=obj.salesforce_url)

    show_salesforce_url.short_description = "Salesforce Link"


class CountryAdmin(AdminForUserMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'name_es', 'name_fr')


class LWRRegionAdmin(AdminForUserMixin, admin.ModelAdmin):
    list_display = ('name', 'subregions')
    list_display_links = ('name',)
    list_per_page = 20
    list_max_show_all = 50
    search_fields = ['name', 'subregions']
    inlines = [
        CountryInline,
    ]
    fieldsets = [
        (_('General information'), {'fields': ['id', 'name', 'subregions']}),
    ]


admin.site.register(Contact, ContactAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(ProjectContact, ProjectContactAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(SubProject, SubprojectAdmin)
admin.site.register(LWRRegion, LWRRegionAdmin)
admin.site.register(Country, CountryAdmin)

models = apps.get_models()
for model in models:
    admin_class = type('AdminClass', (ListAdminMixin, ImportExportModelAdmin), {})
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        pass
