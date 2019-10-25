"""
admin customization for 'monitoring'
"""
from django.apps import apps
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html

from jet.admin import CompactInline
from leaflet.admin import LeafletGeoAdmin

from .models import (Contact, Project, Organization, ProjectContact, Profile, SubProject,
                     LWRRegion, Country, City, Sex, Education, OrganizationType)
from django.contrib.auth.models import Group, User
from .modelForm import GroupAdminForm


# Change default query
class AdminForUserMixin:

    def save_model(self, request, obj, form, change):
        if obj.id and hasattr(obj, 'created_user'):
            obj.created_user = request.user.username
        elif hasattr(obj, 'updated_user'):
            obj.updated_user = request.user.username
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        if request.user:
            return self.model.objects.for_user(request.user)
        return super().get_queryset(request)


# based on
# https://hackernoon.com/automatically-register-all-models-in-django-admin-django-tips-481382cf75e5

class ListAdminMixin:
    def __init__(self, model, admin_site):
        not_allowed = ['password', 'colors']
        self.list_filter = []
        self.list_display = [field.name for field in model._meta.fields
                             if field.name not in not_allowed]
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

    def has_add_permission(self, request, obj=None):
        return False


class CountryInline(CompactInline):
    model = Country
    can_delete = False
    extra = 0


class SubProjectsInline(CompactInline):
    model = SubProject
    can_delete = False
    extra = 0


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0


# Admin Class
class ContactAdmin(AdminForUserMixin, LeafletGeoAdmin):
    list_display = ('id', 'name', 'document', 'country', 'organization', 'type', 'title')
    list_display_links = ['name', 'country', 'type']
    list_per_page = 20
    list_max_show_all = 50
    ordering = ['name']
    readonly_fields = ['created', 'updated', ]
    list_filter = [
        ('country'),
        ('organization__name'),
        'type'
    ]
    inlines = [
        ProjectContactInline,
    ]
    search_fields = ['name', 'country__name', 'document', 'organization__name', 'title']


class ProjectAdmin(AdminForUserMixin, admin.ModelAdmin):
    inlines = [
        SubProjectsInline,
    ]
    list_display = (
        'code', 'name', 'status', 'get_countries', 'lwrregion', 'targetmen', 'targetwomen',
        'get_women', 'get_men', 'get_total')
    list_per_page = 20
    list_max_show_all = 50
    list_display_links = ['name']
    ordering = ['id']
    search_fields = ['code', 'name', ]
    date_hierarchy = 'start'
    readonly_fields = ['created', 'updated', 'show_salesforce_url']
    fieldsets = [
        (_('General information'),
         {'fields': ['code', 'name', 'status', 'logo', 'colors', 'url', 'lwrregion',
                     'show_salesforce_url', 'created', 'updated', ]}),
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


class OrganizationAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'description', 'country', 'organization_parent', 'organization_type',
        'is_implementer')
    list_per_page = 20
    list_max_show_all = 50
    ordering = ['id']
    readonly_fields = ['created', 'updated', ]
    list_filter = [
        ('country'),
        ('organization_type'),
    ]
    search_fields = ['id', 'name', 'description', 'country__name']
    exclude = ['id']

    def organization_parent(self, obj):
        if obj.organization_id is not None:
            return obj.name
        return ''


class ProjectContactAdmin(AdminForUserMixin, admin.ModelAdmin):
    list_display = (
        'id', 'project', 'organization', 'contact', 'get_country_contact', 'date_entry_project',
        'date_end_project',)
    list_display_links = ['id', 'project']
    ordering = ['-date_entry_project']
    readonly_fields = ['created', 'updated', ]
    list_per_page = 20
    raw_id_fields = ('contact',)
    list_max_show_all = 50
    search_fields = ['id', 'project__name', 'contact__name', 'product__name']
    list_filter = [
        ('product'),
        ('contact__country', admin.RelatedOnlyFieldListFilter),
        ('organization', admin.RelatedOnlyFieldListFilter),
    ]

    def get_country_contact(self, obj):
        return obj.contact.country

    get_country_contact.short_description = 'Country'


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
    readonly_fields = ['created', 'updated', 'show_salesforce_url']
    search_fields = ['name', 'code', 'project__name', 'status']
    fieldsets = [
        (_('General information'),
         {'fields': ['code', 'name', 'project', 'status', 'organization', 'country',
                     'show_salesforce_url', 'created', 'updated', ]}),
        (_('Date information'), {'fields': ['start', 'end', ]}),
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


class CityAdmin(AdminForUserMixin, LeafletGeoAdmin):
    list_display = ('name', 'country')
    search_fields = ['name', ]
    list_display_links = ('name',)
    list_per_page = 20
    list_max_show_all = 50
    list_filter = [
        ('country', admin.RelatedOnlyFieldListFilter),
    ]


class CountryAdmin(AdminForUserMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'name_es', 'name_fr')
    readonly_fields = ['id']
    search_fields = ['name', 'name_es', 'name_fr']
    list_display_links = ('name',)
    list_per_page = 20
    list_max_show_all = 50


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


class GeneralCatalogAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'name_es', 'name_fr')
    list_display_links = ('id', 'name',)
    list_per_page = 20
    list_max_show_all = 50
    search_fields = ['name', 'name_es', 'name_fr']


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name', ]
    list_display_links = ('username', 'email',)
    list_per_page = 20
    list_max_show_all = 50
    inlines = [
        ProfileInline
    ]


admin.site.unregister(Group)
admin.site.unregister(User)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(ProjectContact, ProjectContactAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(SubProject, SubprojectAdmin)
admin.site.register(LWRRegion, LWRRegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Sex, GeneralCatalogAdmin)
admin.site.register(Education, GeneralCatalogAdmin)
admin.site.register(OrganizationType, GeneralCatalogAdmin)

MODELS = apps.get_models()
for model in MODELS:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
