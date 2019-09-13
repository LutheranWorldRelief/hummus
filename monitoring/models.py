from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class LWRRegion(models.Model):
    id = models.CharField(primary_key=True, max_length=8, verbose_name=_('Id'))
    name = models.CharField(max_length=20, verbose_name=_('Name'))
    subregions = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Subregions'))

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
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, verbose_name=_('Language'), default='en')
    lwrregions = models.ManyToManyField('LWRRegion', verbose_name=_('LWR Regions'), blank=True)
    countries = models.ManyToManyField('Country', verbose_name=_('Countries'), blank=True)
    projects = models.ManyToManyField('Project', verbose_name=_('Projects'), blank=True)

    def __str__(self):
        return "%s" % (self.user)

    class Meta:
        ordering = ['user']
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')


class Attendance(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, verbose_name=_('Event'))
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name=_('Contact'))
    type = models.ForeignKey('ContactType', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Type'))
    document = models.CharField(max_length=45, blank=True, null=True, verbose_name=_('Document'))
    sex = models.CharField(max_length=1, blank=True, null=True, verbose_name=_('Sex'))
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, verbose_name=_('Country'))
    community = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Community'))
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True, null=True,
                                     verbose_name=_('Organization'))
    phone_personal = models.CharField(max_length=45, blank=True, null=True, verbose_name=_('Phone Personal'))

    def __str__(self):
        return "%s: %s" % (self.event.name, self.contact.name)

    class Meta:
        ordering = ['event', 'contact']
        db_table = 'attendance'
        verbose_name = _('Attendance')
        verbose_name_plural = _('Attendances')


class Contact(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    last_name = models.CharField(max_length=80, blank=True, null=True, verbose_name=_('Last Name'))
    first_name = models.CharField(max_length=80, blank=True, null=True, verbose_name=_('First Name'))
    birthdate = models.DateField(blank=True, null=True, verbose_name=_('Birthdate'))
    document = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Document'))
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Title'))
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True, null=True,
                                     verbose_name=_('Organization'))
    sex = models.CharField(max_length=1, blank=True, null=True, verbose_name=_('Sex'))
    type = models.ForeignKey('ContactType', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Type'))
    community = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Community'))
    municipality = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Municipality'))
    city = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('City'))
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, verbose_name=_('Country'))
    education = models.ForeignKey('Education', on_delete=models.SET_NULL, blank=True, null=True,
                                  verbose_name=_('Education'))
    phone_personal = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone Personal'))
    phone_work = models.CharField(max_length=20, blank=True, null=True, verbose_name=_('Phone Work'))
    men_home = models.IntegerField(blank=True, null=True, verbose_name=_('Men Home'))
    women_home = models.IntegerField(blank=True, null=True, verbose_name=_('Women Home'))
    created = models.DateField(blank=True, null=True, verbose_name=_('Created'))
    modified = models.DateField(blank=True, null=True, verbose_name=_('Modified'))

    def get_absolute_url(self):
        return "/contact/%i/" % self.id

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'contact'
        verbose_name = _('Contact')
        verbose_name_plural = _('Contacts')


class Country(models.Model):
    id = models.CharField(primary_key=True, max_length=2, verbose_name=_('Id'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    name_es = models.CharField(max_length=255, verbose_name=_('Name ES'))
    name_fr = models.CharField(max_length=255, verbose_name=_('Name FR'))
    codigo_numerico = models.IntegerField(verbose_name=_('Numerical Code'))
    alfa3 = models.CharField(max_length=3, verbose_name=_('Alfa3'))
    x = models.CharField(max_length=255, verbose_name=_('X'))
    y = models.CharField(max_length=255, verbose_name=_('Y'))
    region = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Region'))
    subregion = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Sub Region'))
    phonecode = models.CharField(max_length=5, blank=True, null=True, verbose_name=_('Phone Code'))
    lwrregion = models.ForeignKey('LWRRegion', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('LWR Region'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']
        db_table = 'country'
        verbose_name = _('Country')
        verbose_name_plural = _('Countries')


class Event(models.Model):
    structure = models.ForeignKey('Structure', on_delete=models.SET_NULL, blank=True, null=True,
                                  verbose_name=_('Structure'))
    name = models.CharField(max_length=455, verbose_name=_('Name'))
    title = models.TextField(blank=True, null=True, verbose_name=_('Title'))
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True, null=True,
                                     verbose_name=_('Organization'))
    organizer = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Organizer'))
    text = models.TextField(blank=True, null=True, verbose_name=_('Text'))
    start = models.DateTimeField(blank=True, null=True, verbose_name=_('Start'))
    end = models.DateTimeField(blank=True, null=True, verbose_name=_('End'))
    place = models.CharField(max_length=200, blank=True, null=True, verbose_name=_('Place'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('Notes'))
    country = models.ForeignKey('Country', null=True, on_delete=models.SET_NULL, verbose_name=_('Country'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'event'
        verbose_name = _('Event')
        verbose_name_plural = _('Events')


class Filter(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    start = models.CharField(max_length=255, verbose_name=_('Start'))
    end = models.CharField(max_length=255, verbose_name=_('End'))
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


class Organization(models.Model):
    name = models.TextField(verbose_name=_('Name'))
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, verbose_name=_('Country'))
    organization_type = models.ForeignKey('OrganizationType', on_delete=models.SET_NULL, blank=True, null=True,
                                          verbose_name=_('Organization Type'))
    organization = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="parent",
                                     verbose_name=_('Organization'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Description'))
    country_number = models.IntegerField(blank=True, null=True, verbose_name=_('Country Number'))
    is_implementer = models.BooleanField(verbose_name=_('Is Implementer'))

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
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))

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
            elif user.profile.countries.exists():
                return self.filter(countries__in=user.profile.countries.all())
            elif user.profile.projects.exists():
                return self.filter(profile=user.profile)
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
    salesforce = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name=_('Salesforce Id'))
    logo = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Logo'))
    colors = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Colors'))
    url = models.URLField(blank=True, null=True, verbose_name=_('Url'))
    start = models.DateField(blank=True, null=True, verbose_name=_('Start'))
    end = models.DateField(blank=True, null=True, verbose_name=_('End'))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True, verbose_name=_('Status'))
    targetmen = models.IntegerField(blank=True, null=True, db_column='goal_men', verbose_name=_('Target Direct Men'))
    targetwomen = models.IntegerField(blank=True, null=True, db_column='goal_women', verbose_name=_('Target Direct Women'))
    targetimen = models.IntegerField(blank=True, null=True, verbose_name=_('Target Indirect Men'))
    targetiwomen = models.IntegerField(blank=True, null=True, verbose_name=_('Target Indirect Women'))
    countries = models.ManyToManyField('Country', verbose_name=_('Countries'), blank=True)
    lwrregion = models.ForeignKey('LWRRegion', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('LWR Region'))
    recordtype = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Record Type'))

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

    @property
    def salesforce_url(self):
        return '%s/%s' % (settings.SALESFORCE_URL, self.salesforce)

class SubProjectQuerySet(models.QuerySet):
    def for_user(self, user):
        if user.profile.projects.exists():
            return self.filter(project__profile=user.profile)
        else:
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
    salesforce = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name=_('Salesforce Id'))
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name=_('Project'))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True, verbose_name=_('Status'))
    start = models.DateField(blank=True, null=True, verbose_name=_('Start'))
    end = models.DateField(blank=True, null=True, verbose_name=_('End'))
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Country'))
    targetmen = models.IntegerField(blank=True, null=True, verbose_name=_('Target Direct Men'))
    targetwomen = models.IntegerField(blank=True, null=True, verbose_name=_('Target Direct Women'))
    targetimen = models.IntegerField(blank=True, null=True, verbose_name=_('Target Indirect Men'))
    targetiwomen = models.IntegerField(blank=True, null=True, verbose_name=_('Target Indirect Women'))
    recordtype = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Record Type'))

    class Meta:
        ordering = ['name']
        db_table = 'subproject'
        verbose_name = _('Sub Project')
        verbose_name_plural = _('Sub Projects')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/subproject/%i/" % self.id

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


class ProjectContact(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name=_('Project'))
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name=_('Contact'))
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Product'))
    area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_('Area'))
    development_area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                                           verbose_name=_('Development Area'))
    productive_area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                                          verbose_name=_('Productive Area'))
    age_development_plantation = models.IntegerField(blank=True, null=True,
                                                     verbose_name=_('Age Development Plantation'))
    age_productive_plantation = models.IntegerField(blank=True, null=True, verbose_name=_('Age Productive Plantation'))
    yield_field = models.FloatField(db_column='yield', blank=True, null=True, verbose_name=_(
        'Yield Field'))  # Field renamed because it was a Python reserved word.
    date_entry_project = models.DateField(blank=True, null=True, verbose_name=_('Date Entry Project'))
    date_end_project = models.DateField(blank=True, null=True, verbose_name=_('Date End Project'))

    def __str__(self):
        return "%s: %s" % (self.project.name, self.contact.name)

    class Meta:
        ordering = ['project', 'contact']
        db_table = 'project_contact'
        verbose_name = _('Project Contact')
        verbose_name_plural = _('Project Contacts')


class Structure(models.Model):
    code = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Code'))
    description = models.TextField(verbose_name=_('Description'))
    structure = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="parent",
                                  verbose_name=_('Structure'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('Notes'))
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name=_('Project'))

    def __str__(self):
        return "%s: %s" % (self.project.name, self.description)

    class Meta:
        ordering = ['project', 'description']
        db_table = 'structure'
        verbose_name = _('Structure')


class Education(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    name_es = models.CharField(max_length=100, verbose_name=_('Name ES'))
    name_fr = models.CharField(max_length=100, verbose_name=_('Name FR'))

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
