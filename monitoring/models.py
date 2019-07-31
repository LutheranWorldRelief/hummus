from django.db import models


class Attendance(models.Model):
    id = models.IntegerField(primary_key=True)
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    document = models.CharField(max_length=45, blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    community = models.CharField(max_length=255, blank=True, null=True)
    org_id = models.IntegerField(blank=True, null=True)
    phone_personal = models.CharField(max_length=45, blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "%s: %s" % (self.event.name, self.contact.name)

    class Meta:
        ordering = ['event', 'contact']
        db_table = 'attendance'


class Contact(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=80, blank=True, null=True)
    first_name = models.CharField(max_length=80, blank=True, null=True)
    document = models.CharField(max_length=40, blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    organization_id = models.IntegerField(blank=True, null=True)
    sex = models.CharField(max_length=1, blank=True, null=True)
    community = models.CharField(max_length=40, blank=True, null=True)
    municipality = models.CharField(max_length=40, blank=True, null=True)
    city = models.CharField(max_length=40, blank=True, null=True)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    education = models.ForeignKey('Education', on_delete=models.SET_NULL, blank=True, null=True)
    phone_personal = models.CharField(max_length=20, blank=True, null=True)
    phone_work = models.CharField(max_length=20, blank=True, null=True)
    men_home = models.IntegerField(blank=True, null=True)
    women_home = models.IntegerField(blank=True, null=True)
    created = models.DateField(blank=True, null=True)
    modified = models.DateField(blank=True, null=True)
    type_id = models.IntegerField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'contact'


class Country(models.Model):
    id = models.CharField(primary_key=True, max_length=2)
    name = models.CharField(max_length=255)
    name_es = models.CharField(max_length=255)
    codigo_numerico = models.IntegerField()
    alfa3 = models.CharField(max_length=3)
    x = models.CharField(max_length=255)
    y = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name']
        db_table = 'country'


class DataList(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField(blank=True, null=True)
    tag = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=45, blank=True, null=True)
    data_list = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True, null=True)
    slug = models.CharField(max_length=255, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "%s: %s" % (self.id, self.name)

    class Meta:
        ordering = ['id', 'name']
        db_table = 'data_list'



class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    structure_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=455)
    title = models.TextField(blank=True, null=True)
    implementing_organization_id = models.IntegerField()
    organizer = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    place = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    country = models.ForeignKey('Country', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'event'


class Filter(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    start = models.CharField(max_length=255)
    end = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    order = models.IntegerField(blank=True, null=True)
    filter = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="parent")

    def __str__(self):
        return "%s: %s" % (self.slug, self.name)

    class Meta:
        ordering = ['slug', 'name']
        db_table = 'filter'


class Organization(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)
    organization_type_id = models.IntegerField(blank=True, null=True)
    organization_id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    country_number = models.IntegerField(blank=True, null=True)
    is_implementer = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'organization'


class OrganizationType(models.Model):
    id = models.IntegerField(primary_key=True)
    abbreviation = models.CharField(max_length=45)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'organization_type'


class Project(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.TextField()
    code = models.CharField(max_length=255)
    logo = models.CharField(max_length=255, blank=True, null=True)
    colors = models.TextField()
    url = models.CharField(max_length=255, blank=True, null=True)
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)
    goal_men = models.IntegerField(blank=True, null=True)
    goal_women = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'project'


class ProjectContact(models.Model):
    id = models.IntegerField(primary_key=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)
    contact = models.ForeignKey('Contact', on_delete=models.CASCADE)
    product = models.CharField(max_length=255, blank=True, null=True)
    area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    development_area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    productive_area = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    age_development_plantation = models.IntegerField(blank=True, null=True)
    age_productive_plantation = models.IntegerField(blank=True, null=True)
    yield_field = models.FloatField(db_column='yield', blank=True, null=True)  # Field renamed because it was a Python reserved word.
    date_entry_project = models.DateField(blank=True, null=True)
    date_end_project = models.DateField(blank=True, null=True)

    def __str__(self):
        return "%s: %s" % (self.project.name, self.contact.name)

    class Meta:
        ordering = ['project', 'contact']
        db_table = 'project_contact'


class Structure(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField()
    structure = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="parent")
    notes = models.TextField(blank=True, null=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE)

    def __str__(self):
        return "%s: %s" % (self.project.name, self.description)

    class Meta:
        ordering = ['project', 'description']
        db_table = 'structure'


class Education(models.Model):
    name = models.CharField(max_length=100)
    name_es = models.CharField(max_length=100)
    name_fr = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class ContactType(models.Model):
    name = models.CharField(max_length=100)
    name_es = models.CharField(max_length=100)
    name_fr = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
