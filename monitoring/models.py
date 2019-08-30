from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


months = [('1','January'),
    ('2',_('February')),
    ('3',_('March')),
    ('4',_('April')),
    ('5',_('May')),
    ('6',_('June')),
    ('7',_('July')),
    ('8',_('August')),
    ('9',_('September')),
    ('10',_('October')),
    ('11',_('November')),
    ('12',_('December')),]


class Region(models.Model):
    name = models.CharField(max_length=20, verbose_name=_('Name'))

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        ordering = ['name']
        verbose_name=_('Region')


class Profile(models.Model):
    LANGUAGE_CHOICES = [
	('en', 'English'),
	('fr', 'French'),
	('es', 'Spanish'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('User'))
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, verbose_name=_('Language'), default='en')
    regiones = models.ManyToManyField('Region', verbose_name=_('Regions'), blank=True)
    countries = models.ManyToManyField('Country', verbose_name=_('Countries'), blank=True)
    projects = models.ManyToManyField('Project', verbose_name=_('Projects'), blank=True)

    def __str__(self):
        return "%s" % (self.user)

    class Meta:
        ordering = ['user']
        verbose_name=_('Profile')


class Attendance(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=_('Id'))
    event = models.ForeignKey('Event', on_delete=models.CASCADE, verbose_name=_('Event'))
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name=_('Contact'))
    type = models.ForeignKey('ContactType', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Type'))
    document = models.CharField(max_length=45, blank=True, null=True, verbose_name=_('Document'))
    sex = models.CharField(max_length=1, blank=True, null=True, verbose_name=_('Sex'))
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, verbose_name=_('Country'))
    community = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Community'))
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Organization'))
    phone_personal = models.CharField(max_length=45, blank=True, null=True, verbose_name=_('Phone Personal'))

    def __str__(self):
        return "%s: %s" % (self.event.name, self.contact.name)

    class Meta:
        ordering = ['event', 'contact']
        db_table = 'attendance'
        verbose_name=_('Attendance')

class Contact(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=_('Id'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    last_name = models.CharField(max_length=80, blank=True, null=True, verbose_name=_('Last Name'))
    first_name = models.CharField(max_length=80, blank=True, null=True, verbose_name=_('First Name'))
    birthdate = models.DateField(blank=True, null=True, verbose_name=_('Birthdate'))
    document = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Document'))
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name=_('Title'))
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Organization'))
    sex = models.CharField(max_length=1, blank=True, null=True, verbose_name=_('Sex'))
    type = models.ForeignKey('ContactType', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Type'))
    community = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Community'))
    municipality = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Municipality'))
    city = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('City'))
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, verbose_name=_('Country'))
    education = models.ForeignKey('Education', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Education'))
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
        verbose_name=_('Contact')

class Country(models.Model):
    id = models.CharField(primary_key=True, max_length=2, verbose_name=_('Id'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    name_es = models.CharField(max_length=255, verbose_name=_('Name_Es'))
    codigo_numerico = models.IntegerField(verbose_name=_('Numerical Code'))
    alfa3 = models.CharField(max_length=3, verbose_name=_('Alfa3'))
    x = models.CharField(max_length=255, verbose_name=_('X'))
    y = models.CharField(max_length=255, verbose_name=_('Y'))
    region = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('Region'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']
        db_table = 'country'
        verbose_name=_('Country')

class DataList(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=_('Id'))
    name = models.TextField(blank=True, null=True, verbose_name=_('Name'))
    tag = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Tag'))
    value = models.CharField(max_length=45, blank=True, null=True, verbose_name=_('Value'))
    data_list = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, verbose_name=_('Data List'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('Notes'))
    slug = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Slug'))
    order = models.IntegerField(blank=True, null=True, verbose_name=_('Order'))

    def __str__(self):
        return "%s: %s" % (self.id, self.name)

    class Meta:
        ordering = ['id', 'name']
        db_table = 'data_list'
        verbose_name=_('DataList')


class Event(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=_('Id'))
    structure = models.ForeignKey('Structure', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Structure'))
    name = models.CharField(max_length=455, verbose_name=_('Name'))
    title = models.TextField(blank=True, null=True, verbose_name=_('Title'))
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Organization'))
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
        verbose_name=_('Event')

class Filter(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=_('Id'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    start = models.CharField(max_length=255, verbose_name=_('Start'))
    end = models.CharField(max_length=255, verbose_name=_('End'))
    slug = models.CharField(max_length=255, verbose_name=_('Slug'))
    order = models.IntegerField(blank=True, null=True, verbose_name=_('Order'))
    filter = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="parent", verbose_name=_('Filter'))

    def __str__(self):
        return "%s: %s" % (self.slug, self.name)

    class Meta:
        ordering = ['slug', 'name']
        db_table = 'filter'
        verbose_name=_('Filter')

class Organization(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=_('Id'))
    name = models.TextField(verbose_name=_('Name'))
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True, verbose_name=_('Country'))
    organization_type = models.ForeignKey('OrganizationType', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Organization Type'))
    organization = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="parent", verbose_name=_('Organization'))
    description = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Description'))
    country_number = models.IntegerField(blank=True, null=True, verbose_name=_('Country Number'))
    is_implementer = models.BooleanField(verbose_name=_('Is Implementer'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'organization'
        verbose_name=_('Organization')

class OrganizationType(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=_('Id'))
    abbreviation = models.CharField(max_length=45, verbose_name=_('Abbreviation'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'organization_type'
        verbose_name=_('Organization Type')

class Project(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=_('Id'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    code = models.CharField(max_length=255, verbose_name=_('Code'))
    logo = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Logo'))
    colors = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Colors'))
    url = models.URLField(blank=True, null=True, verbose_name=_('Url'))
    start = models.DateField(blank=True, null=True, verbose_name=_('Start'))
    end = models.DateField(blank=True, null=True, verbose_name=_('End'))
    goalmen = models.IntegerField(blank=True, null=True, db_column='goal_men', verbose_name=_('Goal Men'))
    goalwomen = models.IntegerField(blank=True, null=True, db_column='goal_women', verbose_name=_('Goal Women'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'project'
        verbose_name=_('Project')
    def get_absolute_url(self):
        return "/project/%i/" % self.id


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    name_es = models.CharField(max_length=100, verbose_name=_('Name_Es'))
    name_fr = models.CharField(max_length=100, verbose_name=_('Name_Fr'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name=_('Product')

class ProjectContact(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=_('Id'))
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name=_('Project'))
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE, verbose_name=_('Contact'))
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, blank=True, null=True, verbose_name=_('Product'))
    area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_('Area'))
    development_area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_('Development Area'))
    productive_area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name=_('Productive Area'))
    age_development_plantation = models.IntegerField(blank=True, null=True, verbose_name=_('Age Development Plantation'))
    age_productive_plantation = models.IntegerField(blank=True, null=True, verbose_name=_('Age Productive Plantation'))
    yield_field = models.FloatField(db_column='yield', blank=True, null=True, verbose_name=_('Yield Field'))  # Field renamed because it was a Python reserved word.
    date_entry_project = models.DateField(blank=True, null=True, verbose_name=_('Date Entry Project'))
    date_end_project = models.DateField(blank=True, null=True, verbose_name=_('Date End Project'))

    def __str__(self):
        return "%s: %s" % (self.project.name, self.contact.name)

    class Meta:
        ordering = ['project', 'contact']
        db_table = 'project_contact'
        verbose_name=_('Project Contact')

class Structure(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name=_('Id'))
    code = models.CharField(max_length=150, blank=True, null=True, verbose_name=_('Code'))
    description = models.TextField(verbose_name=_('Description'))
    structure = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="parent", verbose_name=_('Structure'))
    notes = models.TextField(blank=True, null=True, verbose_name=_('Notes'))
    project = models.ForeignKey('Project', on_delete=models.CASCADE, verbose_name=_('Project'))

    def __str__(self):
        return "%s: %s" % (self.project.name, self.description)

    class Meta:
        ordering = ['project', 'description']
        db_table = 'structure'
        verbose_name=_('Structure')

class Education(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    name_es = models.CharField(max_length=100, verbose_name=_('Name_Es'))
    name_fr = models.CharField(max_length=100, verbose_name=_('Name_Fr'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name=_('Education')

class ContactType(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    name_es = models.CharField(max_length=100, verbose_name=_('Name_Es'))
    name_fr = models.CharField(max_length=100, verbose_name=_('Name_Fr'))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name=_('Contact Type')
