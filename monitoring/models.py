"""
participant tracking data models
"""

from django.db import models
from django.db.models import Sum, Count, Q
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.gis.db import models as geomodels
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import PermissionDenied
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from .common import xstr


class Request(models.Model):
    meta = models.TextField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    created_user = models.CharField(max_length=64, null=True, blank=True,
                                    verbose_name=_('Created by'))
    source = models.ForeignKey('Source', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_('Data Source'))


class Template(models.Model):
    id = models.CharField(primary_key=True, max_length=32, verbose_name=_('Filename'))
    name = models.CharField(max_length=50, verbose_name=_('Name'))
    name_fr = models.CharField(max_length=50, verbose_name=_('Name FR'))
    name_es = models.CharField(max_length=50, verbose_name=_('Name ES'))
    file = models.FileField(upload_to='templates/', verbose_name=_('File'), null=True, blank=True)
    file_fr = models.FileField(upload_to='templates/', verbose_name=_('File FR'),
                               null=True, blank=True)
    file_es = models.FileField(upload_to='templates/', verbose_name=_('File ES'),
                               null=True, blank=True)
    mapping = JSONField(null=True, blank=True, verbose_name=_('Mapping'))
    mapping_fr = JSONField(null=True, blank=True, verbose_name=_('Mapping FR'))
    mapping_es = JSONField(null=True, blank=True, verbose_name=_('Mapping ES'))

    def __str__(self):
        return "%s: %s" % (self.name, self.id)

    class Meta:
        ordering = ['name']
        verbose_name = _('Template')
        verbose_name_plural = _('Templates')
        db_table = 'template'


class LWRRegionQuerySet(models.QuerySet):
    def for_user(self, user):
        if hasattr(user, 'profile'):
            if user.profile.lwrregions.exists():
                return user.profile.lwrregions
        else:
            raise PermissionDenied(_("Current user has no profile."))
        return self


class LWRRegion(models.Model):
    id = models.CharField(primary_key=True, max_length=8, verbose_name=_('Id'))
    name = models.CharField(max_length=20, verbose_name=_('Name'))
    subregions = models.CharField(max_length=200, blank=True, null=True,
                                  verbose_name=_('Subregions'))

    objects = LWRRegionQuerySet.as_manager()

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        ordering = ['name']
        verbose_name = _('LWR Region')
        verbose_name_plural = _('LWR Regions')
        db_table = 'lwrregion'


class Profile(models.Model):
    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('fr', _('French')),
        ('es', _('Spanish')),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES,
                                verbose_name=_('Language'), default='en')
    lwrregions = models.ManyToManyField('LWRRegion', verbose_name=_('LWR Regions'), blank=True)
    countries = models.ManyToManyField('Country', verbose_name=_('Countries'), blank=True)
    projects = models.ManyToManyField('Project', verbose_name=_('Projects'), blank=True)

    def __str__(self):
        return "%s" % (self.user)

    class Meta:
        ordering = ['user']
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


class Sex(models.Model):
    id = models.CharField(primary_key=True, max_length=1, verbose_name=_('Id'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    varname = models.CharField(max_length=255, verbose_name=_('Variable Id'))
    name_es = models.CharField(max_length=255, verbose_name=_('Name ES'))
    varname_es = models.CharField(max_length=255, verbose_name=_('Variable Id ES'))
    name_fr = models.CharField(max_length=255, verbose_name=_('Name FR'))
    varname_fr = models.CharField(max_length=255, verbose_name=_('Variable Id FR'))

    def __str__(self):
        return "%s" % (self.id)

    class Meta:
        ordering = ['id']
        verbose_name = _('Sex')
        verbose_name_plural = _('Sex')


class Source(models.Model):
    id = models.CharField(primary_key=True, max_length=16, verbose_name=_('Id'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = _('Data Source')
        verbose_name_plural = _('Data Sources')


class CountryNE(models.Model):
    iso_a2 = models.CharField(max_length=2, null=True, blank=True)
    sov_a3 = models.CharField(max_length=3, null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name=_('Name'), null=True, blank=True)
    name_es = models.CharField(max_length=255, verbose_name=_('Name ES'), null=True, blank=True)
    name_fr = models.CharField(max_length=255, verbose_name=_('Name FR'), null=True, blank=True)
    geometry = geomodels.MultiPolygonField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        db_table = 'countryne'


class CityQuerySet(models.QuerySet):
    def for_user(self, user):
        if hasattr(user, 'profile'):
            if user.profile.countries.exists():
                return City.objects.filter(country__in=user.profile.countries.all())
        else:
            raise PermissionDenied(_("Current user has no profile."))
        return self


class City(models.Model):
    name = models.CharField(max_length=100, blank=False)
    location = geomodels.PointField()
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_('Country'))

    objects = CityQuerySet.as_manager()

    def __str__(self):
        return "{}, {}".format(self.name, self.country.name)

    def get_absolute_url(self):
        return "/city/%i/" % self.id

    class Meta:
        ordering = ('name',)
        verbose_name_plural = _('Cities')
        db_table = 'city'


class ContactQuerySet(models.QuerySet):
    def for_user(self, user):
        if hasattr(user, 'profile'):
            if user.profile.lwrregions.exists():
                return self.filter(projectcontact__project__countries__lwrregion__in=user.profile.lwrregions.all())
            if user.profile.countries.exists():
                return self.filter(projectcontact__project__countries__in=user.profile.countries.all())
            if user.profile.projects.exists():
                return self.filter(projectcontact__project__in=user.profile.projects.all())
        else:
            raise PermissionDenied(_("Current user has no profile."))
        return self


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    last_name = models.CharField(max_length=80, blank=True, null=True, verbose_name=_('Last Name'))
    first_name = models.CharField(max_length=80, blank=True, null=True,
                                  verbose_name=_('First Name'))
    birthdate = models.DateField(blank=True, null=True, verbose_name=_('Birthdate'))
    document = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Document'))
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Title'))
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True,
                                     null=True, verbose_name=_('Organization'))
    sex = models.ForeignKey('Sex', on_delete=models.SET_NULL, blank=True, null=True,
                            verbose_name=_('Sex'))
    type = models.ForeignKey('ContactType', on_delete=models.SET_NULL, blank=True, null=True,
                             verbose_name=_('Type'))
    community = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Community'))
    municipality = models.CharField(max_length=40, blank=True, null=True,
                                    verbose_name=_('Municipality'))
    city = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('City'))
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True,
                                verbose_name=_('Country'))
    education = models.ForeignKey('Education', on_delete=models.SET_NULL, blank=True, null=True,
                                  verbose_name=_('Education'))
    phone_personal = models.CharField(max_length=20, blank=True, null=True,
                                      verbose_name=_('Phone Personal'))
    phone_work = models.CharField(max_length=20, blank=True, null=True,
                                  verbose_name=_('Phone Work'))
    men_home = models.IntegerField(blank=True, null=True, verbose_name=_('Men Home'))
    women_home = models.IntegerField(blank=True, null=True, verbose_name=_('Women Home'))
    location = geomodels.PointField(verbose_name=_('Location'), blank=True, null=True)

    # Contact meta data fields
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Modified'))
    created_user = models.CharField(max_length=64, null=True, blank=True,
                                    verbose_name=_('Created by'))
    updated_user = models.CharField(max_length=64, null=True, blank=True,
                                    verbose_name=_('Modified by'))
    source = models.ForeignKey('Source', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_('Data Source'))

    objects = ContactQuerySet.as_manager()

    def get_absolute_url(self):
        return "/contact/%i/" % self.id

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        # strips stuff from text fields, and detects snake_names
        for field in self._meta.get_fields():
            if isinstance(field, models.CharField):
                value = getattr(self, field.name)
                if value:
                    value = str(value).strip()
                    # detect snake_name, change to Snake Name
                    simple_value = value
                    simple_value = simple_value.replace(' ', '')
                    simple_value = simple_value.replace('_', '')
                    if '_' in value and all(c.islower() for c in simple_value):
                        value = value.replace('_', ' ').title()

                    setattr(self, field.name, value)

        # compute  'name' from first and last name, if needed
        if not self.name and (self.first_name or self.last_name):
            self.name = "{} {}".format(xstr(self.first_name), xstr(self.last_name))
            self.name = self.name.strip()
        elif not self.name:
            raise ValueError(_("We need a name! name, first_name and last_name seem to be empty."))

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        db_table = 'contact'
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')


class CountryQuerySet(models.QuerySet):
    def for_user(self, user):
        if hasattr(user, 'profile'):
            if user.profile.countries.exists():
                return user.profile.countries
        else:
            raise PermissionDenied(_("Current user has no profile."))
        return self


class Country(models.Model):
    id = models.CharField(primary_key=True, max_length=2, verbose_name=_('Id'))
    name = models.CharField(max_length=255, verbose_name=_('Name'), unique=True)
    name_es = models.CharField(max_length=255, verbose_name=_('Name ES'), unique=True)
    name_fr = models.CharField(max_length=255, verbose_name=_('Name FR'), unique=True)
    codigo_numerico = models.IntegerField(verbose_name=_('Numerical Code'), null=True, blank=True)
    alfa3 = models.CharField(max_length=3, verbose_name=_('Alfa3'))
    x = models.CharField(max_length=255, verbose_name=_('X'), null=True, blank=True)
    y = models.CharField(max_length=255, verbose_name=_('Y'), null=True, blank=True)
    region = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Region'))
    subregion = models.CharField(max_length=255, blank=True, null=True,
                                 verbose_name=_('Sub Region'))
    phonecode = models.CharField(max_length=5, blank=True, null=True, verbose_name=_('Phone Code'))
    lwrregion = models.ForeignKey('LWRRegion', on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name=_('LWR Region'))

    objects = CountryQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']
        db_table = 'country'
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class Filter(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    start = models.IntegerField(verbose_name=_('Start'))
    end = models.IntegerField(verbose_name=_('End'))
    slug = models.CharField(max_length=255, verbose_name=_('Slug'))
    order = models.IntegerField(blank=True, null=True, verbose_name=_('Order'))
    filter = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="parent",
                               verbose_name=_('Filter'))

    def __str__(self):
        return "%s: %s" % (self.slug, self.name)

    class Meta:
        ordering = ['slug', 'name']
        db_table = 'filter'
        verbose_name = _('Filter')
        verbose_name_plural = _('Filters')


class OrganizationQuerySet(models.QuerySet):
    def for_user(self, user):
        if hasattr(user, 'profile'):
            if user.profile.lwrregions.exists():
                return self.filter(country__lwrregion__in=user.profile.lwrregions.all())
            if user.profile.countries.exists():
                return self.filter(country__in=user.profile.countries.all())
        else:
            raise PermissionDenied(_("Current user has no profile."))
        return self


class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True,
                                verbose_name=_('Country'))
    organization_type = models.ForeignKey('OrganizationType', on_delete=models.SET_NULL, blank=True,
                                          null=True, verbose_name=_('Organization Type'))
    organization = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
                                     related_name="parent", verbose_name=_('Organization'))
    description = models.CharField(max_length=255, blank=True, null=True,
                                   verbose_name=_('Description'))
    country_number = models.IntegerField(blank=True, null=True, verbose_name=_('Country Number'))
    is_implementer = models.BooleanField(default=False, verbose_name=_('Is Implementer'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Modified'))
    created_user = models.CharField(max_length=64, null=True, blank=True,
                                    verbose_name=_('Created by'))
    updated_user = models.CharField(max_length=64, null=True, blank=True,
                                    verbose_name=_('Modified by'))
    source = models.ForeignKey('Source', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_('Data Source'))

    objects = OrganizationQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'organization'
        verbose_name = _('Organization')
        verbose_name_plural = _('Organizations')


class OrganizationType(models.Model):
    abbreviation = models.CharField(max_length=45, verbose_name=_('Abbreviation'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    name_es = models.CharField(max_length=255, verbose_name=_('Name ES'))
    name_fr = models.CharField(max_length=255, verbose_name=_('Name FR'))
    description = models.CharField(max_length=255, blank=True, null=True,
                                   verbose_name=_('Description'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'organization_type'
        verbose_name = _('Organization Type')
        verbose_name_plural = _('Organization Types')


class ProjectQuerySet(models.QuerySet):
    def for_user(self, user):
        if hasattr(user, 'profile'):
            if user.profile.lwrregions.exists():
                return self.filter(lwrregion__in=user.profile.lwrregions.all())
            if user.profile.countries.exists():
                return self.filter(countries__in=user.profile.countries.all())
            if user.profile.projects.exists():
                return self.filter(profile=user.profile)
        else:
            raise PermissionDenied(_("Current user has no profile."))
        return self


class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    STATUS_CHOICES = [
        ('In Development', _('In Development')),
        ('Active', _('Active')),
        ('Inactive', _('Inactive')),
        ('Closed', _('Closed')),
        ('Suspended', _('Suspended')),
        ('Terminated', _('Terminated')),
    ]
    code = models.CharField(max_length=255, unique=True, verbose_name=_('Code'))
    salesforce = models.CharField(max_length=255, null=True, blank=True, unique=True,
                                  verbose_name=_('Salesforce Id'))
    logo = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Logo'))
    colors = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Colors'))
    url = models.URLField(blank=True, null=True, verbose_name=_('Url'))
    start = models.DateField(blank=True, null=True, verbose_name=_('Start'))
    end = models.DateField(blank=True, null=True, verbose_name=_('End'))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True,
                              verbose_name=_('Status'))
    actualmen = models.IntegerField(blank=True, null=True, verbose_name=_('Actual Direct Men'))
    actualwomen = models.IntegerField(blank=True, null=True, verbose_name=_('Actual Direct Women'))
    actualimen = models.IntegerField(blank=True, null=True, verbose_name=_('Actual Indirect Men'))
    actualiwomen = models.IntegerField(blank=True, null=True,
                                       verbose_name=_('Actual Indirect Women'))
    targetmen = models.IntegerField(blank=True, null=True, db_column='goal_men',
                                    verbose_name=_('Target Direct Men'))
    targetwomen = models.IntegerField(blank=True, null=True, db_column='goal_women',
                                      verbose_name=_('Target Direct Women'))
    targetimen = models.IntegerField(blank=True, null=True, verbose_name=_('Target Indirect Men'))
    targetiwomen = models.IntegerField(blank=True, null=True,
                                       verbose_name=_('Target Indirect Women'))
    countries = models.ManyToManyField('Country', verbose_name=_('Countries'), blank=True)
    lwrregion = models.ForeignKey('LWRRegion', on_delete=models.SET_NULL, null=True, blank=True,
                                  verbose_name=_('LWR Region'))
    recordtype = models.CharField(max_length=100, null=True, blank=True,
                                  verbose_name=_('Record Type'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Modified'))
    created_user = models.CharField(max_length=64, null=True, blank=True,
                                    verbose_name=_('Created by'))
    updated_user = models.CharField(max_length=64, null=True, blank=True,
                                    verbose_name=_('Modified by'))
    source = models.ForeignKey('Source', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_('Data Source'))

    objects = ProjectQuerySet.as_manager()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'project'
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')

    def get_absolute_url(self):
        return "/project/%i/" % self.id

    def get_women(self):
        return self.subproject_set.aggregate(women=Sum('actualwomen')).get('women') or 0

    get_women.short_description = _('Women')

    def get_men(self):
        return self.subproject_set.aggregate(men=Sum('actualmen')).get('men') or 0

    get_men.short_description = _('Men')

    def get_total(self):
        return self.get_women() + self.get_men()

    get_total.short_description = _('Total')

    @property
    def salesforce_url(self):
        return '%s/%s' % (settings.SALESFORCE_URL, self.salesforce)


class SubProjectQuerySet(models.QuerySet):
    def for_user(self, user):
        if hasattr(user, 'profile'):
            if user.profile.lwrregions.exists():
                return self.filter(project__lwrregion__in=user.profile.lwrregions.all())
            if user.profile.countries.exists():
                return self.filter(project__countries__in=user.profile.countries.all())
            if user.profile.projects.exists():
                return self.filter(project__profile=user.profile)
        else:
            raise PermissionDenied(_("Current user has no profile."))
        return self


class SubProject(models.Model):
    STATUS_CHOICES = [
        ('Proposed', _('Proposed')),
        ('Active', _('Active')),
        ('Inactive', _('Inactive')),
        ('Suspended', _('Suspended')),
        ('Terminated', _('Terminated')),
        ('Closed', _('Closed')),
    ]
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    code = models.CharField(max_length=255, unique=False, verbose_name=_('Code'))
    salesforce = models.CharField(max_length=255, null=True, blank=True, unique=True,
                                  verbose_name=_('Salesforce Id'))
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name=_('Project'))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True,
                              verbose_name=_('Status'))
    start = models.DateField(blank=True, null=True, verbose_name=_('Start'))
    end = models.DateField(blank=True, null=True, verbose_name=_('End'))
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True,
                                verbose_name=_('Country'))
    actualmen = models.IntegerField(blank=True, null=True, verbose_name=_('Actual Direct Men'))
    actualwomen = models.IntegerField(blank=True, null=True, verbose_name=_('Actual Direct Women'))
    actualimen = models.IntegerField(blank=True, null=True, verbose_name=_('Actual Indirect Men'))
    actualiwomen = models.IntegerField(blank=True, null=True,
                                       verbose_name=_('Actual Indirect Women'))
    targetmen = models.IntegerField(blank=True, null=True, verbose_name=_('Target Direct Men'))
    targetwomen = models.IntegerField(blank=True, null=True, verbose_name=_('Target Direct Women'))
    targetimen = models.IntegerField(blank=True, null=True, verbose_name=_('Target Indirect Men'))
    targetiwomen = models.IntegerField(blank=True, null=True,
                                       verbose_name=_('Target Indirect Women'))
    recordtype = models.CharField(max_length=100, null=True, blank=True,
                                  verbose_name=_('Record Type'))
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True,
                                     null=True, verbose_name=_('Implementing Organization'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Modified'))
    created_user = models.CharField(max_length=64, null=True, blank=True,
                                    verbose_name=_('Created by'))
    updated_user = models.CharField(max_length=64, null=True, blank=True,
                                    verbose_name=_('Modified by'))
    source = models.ForeignKey('Source', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_('Data Source'))

    objects = SubProjectQuerySet.as_manager()

    class Meta:
        ordering = ['name']
        db_table = 'subproject'
        verbose_name = _('Sub Project')
        verbose_name_plural = _('Sub Projects')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/subproject/%i/" % self.id

    @cached_property
    def get_totals(self):
        totals = ProjectContact.objects.filter(project_id=self.project_id).aggregate(
            f=Count('contact', filter=Q(contact__sex='F')),
            m=Count('contact', filter=Q(contact__sex='M')))
        return totals

    @property
    def salesforce_url(self):
        return '%s/%s' % (settings.SALESFORCE_URL, self.salesforce)


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    name_es = models.CharField(max_length=100, verbose_name=_('Name ES'))
    name_fr = models.CharField(max_length=100, verbose_name=_('Name FR'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class ProjectContactQuerySet(models.QuerySet):
    def for_user(self, user):
        if hasattr(user, 'profile'):
            if user.profile.lwrregions.exists():
                return self.filter(project__countries__lwrregion__in=user.profile.lwrregions.all())
            if user.profile.countries.exists():
                return self.filter(project__countries__in=user.profile.countries.all())
            if user.profile.projects.exists():
                return self.filter(project__in=user.profile.projects.all())
        else:
            raise PermissionDenied(_("Current user has no profile."))
        return self


class ProjectContact(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name=_('Project'))
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name=_('Contact'))
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True,
                                verbose_name=_('Product'))
    area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                               verbose_name=_('Area'))
    development_area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                                           verbose_name=_('Development Area'))
    productive_area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                                          verbose_name=_('Productive Area'))
    age_development_plantation = models.IntegerField(blank=True, null=True,
                                                     verbose_name=_('Age Development Plantation'))
    age_productive_plantation = models.IntegerField(blank=True, null=True,
                                                    verbose_name=_('Age Productive Plantation'))
    yield_field = models.FloatField(db_column='yield', blank=True, null=True,
                                    verbose_name=_('Yield Field'))  # renamed: Python reserved word
    date_entry_project = models.DateField(blank=True, null=True,
                                          verbose_name=_('Date Entry Project'))
    date_end_project = models.DateField(blank=True, null=True, verbose_name=_('Date End Project'))
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True,
                                     null=True, verbose_name=_('Organization'))
    extra = JSONField(null=True, blank=True, verbose_name=_('Extra Data'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('Modified'))
    created_user = models.CharField(max_length=64, null=True, blank=True,
                                    verbose_name=_('Created by'))
    updated_user = models.CharField(max_length=64, null=True, blank=True,
                                    verbose_name=_('Modified by'))
    source = models.ForeignKey('Source', on_delete=models.SET_NULL, null=True, blank=True,
                               verbose_name=_('Data Source'))

    objects = ProjectContactQuerySet.as_manager()

    def __str__(self):
        return "%s: %s" % (self.project.name, self.contact.name)

    class Meta:
        ordering = ['project', 'contact']
        db_table = 'project_contact'
        verbose_name = _('Project Contact')
        verbose_name_plural = _('Project Contacts')


class Education(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    varname = models.CharField(max_length=100, verbose_name=_('Variable Id'))
    name_es = models.CharField(max_length=100, verbose_name=_('Name ES'))
    varname_es = models.CharField(max_length=100, verbose_name=_('Variable Id ES'))
    name_fr = models.CharField(max_length=100, verbose_name=_('Name FR'))
    varname_fr = models.CharField(max_length=100, verbose_name=_('Variable Id FR'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Education')
        verbose_name_plural = _('Educations')


class ContactType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    name_es = models.CharField(max_length=100, verbose_name=_('Name ES'))
    name_fr = models.CharField(max_length=100, verbose_name=_('Name FR'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = _('Contact Type')
        verbose_name_plural = _('Contacts Types')


class Log(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('Created'))
    user = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('User'))
    module = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Module'))
    content = models.TextField(blank=True, null=True, verbose_name=_('Content'))
