# Generated by Django 2.2.4 on 2019-09-04 03:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0051_auto_20190824_0738'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'ordering': ['event', 'contact'], 'verbose_name': 'Attendance'},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['name'], 'verbose_name': 'Contact', 'verbose_name_plural': 'Contacts'},
        ),
        migrations.AlterModelOptions(
            name='contacttype',
            options={'ordering': ['name'], 'verbose_name': 'Contact Type'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['name'], 'verbose_name': 'Country', 'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='education',
            options={'ordering': ['name'], 'verbose_name': 'Education'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['name'], 'verbose_name': 'Event'},
        ),
        migrations.AlterModelOptions(
            name='filter',
            options={'ordering': ['slug', 'name'], 'verbose_name': 'Filter'},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name'], 'verbose_name': 'Organization'},
        ),
        migrations.AlterModelOptions(
            name='organizationtype',
            options={'ordering': ['name'], 'verbose_name': 'Organization Type'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'verbose_name': 'Product'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['user'], 'verbose_name': 'Profile'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['name'], 'verbose_name': 'Project'},
        ),
        migrations.AlterModelOptions(
            name='projectcontact',
            options={'ordering': ['project', 'contact'], 'verbose_name': 'Project Contact'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ['name'], 'verbose_name': 'Region'},
        ),
        migrations.AlterModelOptions(
            name='structure',
            options={'ordering': ['project', 'description'], 'verbose_name': 'Structure'},
        ),
        migrations.AlterField(
            model_name='attendance',
            name='community',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Community'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Contact', verbose_name='Contact'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Country', verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='document',
            field=models.CharField(blank=True, max_length=45, null=True, verbose_name='Document'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Event', verbose_name='Event'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Organization', verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='phone_personal',
            field=models.CharField(blank=True, max_length=45, null=True, verbose_name='Phone Personal'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='sex',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='attendance',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.ContactType', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='birthdate',
            field=models.DateField(blank=True, null=True, verbose_name='Birthdate'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='city',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='City'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='community',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Community'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Country', verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='created',
            field=models.DateField(blank=True, null=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='document',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Document'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='education',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Education', verbose_name='Education'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='first_name',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='last_name',
            field=models.CharField(blank=True, max_length=80, null=True, verbose_name='Last Name'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='men_home',
            field=models.IntegerField(blank=True, null=True, verbose_name='Men Home'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='modified',
            field=models.DateField(blank=True, null=True, verbose_name='Modified'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='municipality',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Municipality'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Organization', verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_personal',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Personal'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='phone_work',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Work'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='sex',
            field=models.CharField(blank=True, max_length=1, null=True, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.ContactType', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='women_home',
            field=models.IntegerField(blank=True, null=True, verbose_name='Women Home'),
        ),
        migrations.AlterField(
            model_name='contacttype',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='contacttype',
            name='name_es',
            field=models.CharField(max_length=100, verbose_name='Name_Es'),
        ),
        migrations.AlterField(
            model_name='contacttype',
            name='name_fr',
            field=models.CharField(max_length=100, verbose_name='Name_Fr'),
        ),
        migrations.AlterField(
            model_name='country',
            name='alfa3',
            field=models.CharField(max_length=3, verbose_name='Alfa3'),
        ),
        migrations.AlterField(
            model_name='country',
            name='codigo_numerico',
            field=models.IntegerField(verbose_name='Numerical Code'),
        ),
        migrations.AlterField(
            model_name='country',
            name='id',
            field=models.CharField(max_length=2, primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name_es',
            field=models.CharField(max_length=255, verbose_name='Name_Es'),
        ),
        migrations.AlterField(
            model_name='country',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Region', verbose_name='Region'),
        ),
        migrations.AlterField(
            model_name='country',
            name='x',
            field=models.CharField(max_length=255, verbose_name='X'),
        ),
        migrations.AlterField(
            model_name='country',
            name='y',
            field=models.CharField(max_length=255, verbose_name='Y'),
        ),
        migrations.AlterField(
            model_name='education',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='education',
            name='name_es',
            field=models.CharField(max_length=100, verbose_name='Name_Es'),
        ),
        migrations.AlterField(
            model_name='education',
            name='name_fr',
            field=models.CharField(max_length=100, verbose_name='Name_Fr'),
        ),
        migrations.AlterField(
            model_name='event',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Country', verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='End'),
        ),
        migrations.AlterField(
            model_name='event',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=455, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='event',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='event',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Organization', verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Organizer'),
        ),
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Place'),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start'),
        ),
        migrations.AlterField(
            model_name='event',
            name='structure',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Structure', verbose_name='Structure'),
        ),
        migrations.AlterField(
            model_name='event',
            name='text',
            field=models.TextField(blank=True, null=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='event',
            name='title',
            field=models.TextField(blank=True, null=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='end',
            field=models.CharField(max_length=255, verbose_name='End'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='filter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='monitoring.Filter', verbose_name='Filter'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='order',
            field=models.IntegerField(blank=True, null=True, verbose_name='Order'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='slug',
            field=models.CharField(max_length=255, verbose_name='Slug'),
        ),
        migrations.AlterField(
            model_name='filter',
            name='start',
            field=models.CharField(max_length=255, verbose_name='Start'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Country', verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='country_number',
            field=models.IntegerField(blank=True, null=True, verbose_name='Country Number'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='is_implementer',
            field=models.BooleanField(verbose_name='Is Implementer'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.TextField(verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='organization',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='monitoring.Organization', verbose_name='Organization'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='organization_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.OrganizationType', verbose_name='Organization Type'),
        ),
        migrations.AlterField(
            model_name='organizationtype',
            name='abbreviation',
            field=models.CharField(max_length=45, verbose_name='Abbreviation'),
        ),
        migrations.AlterField(
            model_name='organizationtype',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='organizationtype',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='organizationtype',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_es',
            field=models.CharField(max_length=100, verbose_name='Name_Es'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name_fr',
            field=models.CharField(max_length=100, verbose_name='Name_Fr'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='countries',
            field=models.ManyToManyField(blank=True, to='monitoring.Country', verbose_name='Countries'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='language',
            field=models.CharField(choices=[('en', 'English'), ('fr', 'French'), ('es', 'Spanish')], default='en', max_length=2, verbose_name='Language'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='projects',
            field=models.ManyToManyField(blank=True, to='monitoring.Project', verbose_name='Projects'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='regiones',
            field=models.ManyToManyField(blank=True, to='monitoring.Region', verbose_name='Regions'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
        migrations.AlterField(
            model_name='project',
            name='code',
            field=models.CharField(max_length=255, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='project',
            name='colors',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Colors'),
        ),
        migrations.AlterField(
            model_name='project',
            name='end',
            field=models.DateField(blank=True, null=True, verbose_name='End'),
        ),
        migrations.AlterField(
            model_name='project',
            name='goalmen',
            field=models.IntegerField(blank=True, db_column='goal_men', null=True, verbose_name='Goal Men'),
        ),
        migrations.AlterField(
            model_name='project',
            name='goalwomen',
            field=models.IntegerField(blank=True, db_column='goal_women', null=True, verbose_name='Goal Women'),
        ),
        migrations.AlterField(
            model_name='project',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='project',
            name='logo',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='start',
            field=models.DateField(blank=True, null=True, verbose_name='Start'),
        ),
        migrations.AlterField(
            model_name='project',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='Url'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='age_development_plantation',
            field=models.IntegerField(blank=True, null=True, verbose_name='Age Development Plantation'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='age_productive_plantation',
            field=models.IntegerField(blank=True, null=True, verbose_name='Age Productive Plantation'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='area',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Area'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Contact', verbose_name='Contact'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='date_end_project',
            field=models.DateField(blank=True, null=True, verbose_name='Date End Project'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='date_entry_project',
            field=models.DateField(blank=True, null=True, verbose_name='Date Entry Project'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='development_area',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Development Area'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Product', verbose_name='Product'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='productive_area',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Productive Area'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='yield_field',
            field=models.FloatField(blank=True, db_column='yield', null=True, verbose_name='Yield Field'),
        ),
        migrations.AlterField(
            model_name='region',
            name='name',
            field=models.CharField(max_length=20, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='code',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Id'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Project', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='structure',
            name='structure',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='monitoring.Structure', verbose_name='Structure'),
        ),
        migrations.DeleteModel(
            name='DataList',
        ),
    ]
