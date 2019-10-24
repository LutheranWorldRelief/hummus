# Generated by Django 2.2.6 on 2019-10-24 19:51

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('monitoring', '0001_initial'), ('monitoring', '0002_auto_20190729_1341'), ('monitoring', '0003_auto_20190729_1352'), ('monitoring', '0004_auto_20190729_1356'), ('monitoring', '0005_auto_20190729_1359'), ('monitoring', '0006_auto_20190729_1400'), ('monitoring', '0007_auto_20190729_1453'), ('monitoring', '0008_auto_20190729_1454'), ('monitoring', '0009_auto_20190729_1500'), ('monitoring', '0010_auto_20190729_1504'), ('monitoring', '0011_auto_20190729_1751'), ('monitoring', '0012_auto_20190729_1753'), ('monitoring', '0013_structure_project'), ('monitoring', '0014_auto_20190729_1819'), ('monitoring', '0015_auto_20190729_1820'), ('monitoring', '0016_auto_20190729_1821'), ('monitoring', '0017_auto_20190729_1821'), ('monitoring', '0018_auto_20190729_1822'), ('monitoring', '0019_auto_20190729_1822'), ('monitoring', '0020_auto_20190729_1823'), ('monitoring', '0021_auto_20190729_1824'), ('monitoring', '0022_auto_20190729_1825'), ('monitoring', '0023_auto_20190729_1903'), ('monitoring', '0024_auto_20190729_1914'), ('monitoring', '0025_auto_20190729_1915'), ('monitoring', '0026_auto_20190731_1511'), ('monitoring', '0027_auto_20190731_1512'), ('monitoring', '0028_auto_20190731_1704'), ('monitoring', '0029_contacttype'), ('monitoring', '0030_auto_20190731_1748'), ('monitoring', '0031_auto_20190731_1749'), ('monitoring', '0032_auto_20190731_2011'), ('monitoring', '0033_auto_20190731_2023'), ('monitoring', '0034_auto_20190801_1614'), ('monitoring', '0035_auto_20190801_1615'), ('monitoring', '0036_auto_20190801_1708'), ('monitoring', '0037_auto_20190801_1710'), ('monitoring', '0038_auto_20190801_1725'), ('monitoring', '0039_auto_20190801_1727'), ('monitoring', '0040_auto_20190801_1728'), ('monitoring', '0041_auto_20190812_1432'), ('monitoring', '0042_auto_20190812_1434'), ('monitoring', '0043_auto_20190812_1531'), ('monitoring', '0044_auto_20190812_1532'), ('monitoring', '0045_auto_20190815_0531'), ('monitoring', '0046_auto_20190815_0545'), ('monitoring', '0047_auto_20190817_0404'), ('monitoring', '0048_auto_20190820_1840'), ('monitoring', '0049_auto_20190820_1847'), ('monitoring', '0050_auto_20190820_1848'), ('monitoring', '0051_auto_20190824_0738'), ('monitoring', '0052_auto_20190904_0321'), ('monitoring', '0053_auto_20190904_1725'), ('monitoring', '0054_project_countries'), ('monitoring', '0055_auto_20190906_1836'), ('monitoring', '0056_auto_20190908_0644'), ('monitoring', '0057_auto_20190908_0656'), ('monitoring', '0058_auto_20190908_0702'), ('monitoring', '0059_region_subregions'), ('monitoring', '0060_auto_20190909_0716'), ('monitoring', '0061_project_salesforce'), ('monitoring', '0062_subproject'), ('monitoring', '0063_auto_20190909_1515'), ('monitoring', '0064_auto_20190909_1516'), ('monitoring', '0065_auto_20190909_1516'), ('monitoring', '0066_auto_20190909_1646'), ('monitoring', '0067_auto_20190909_1648'), ('monitoring', '0068_auto_20190909_1713'), ('monitoring', '0069_auto_20190909_1714'), ('monitoring', '0070_auto_20190909_1720'), ('monitoring', '0071_auto_20190909_1737'), ('monitoring', '0072_remove_country_lwrregion'), ('monitoring', '0073_country_lwrregion'), ('monitoring', '0074_remove_profile_lwrregions'), ('monitoring', '0075_profile_lwrregions'), ('monitoring', '0076_project_lwrregion'), ('monitoring', '0077_auto_20190911_1307'), ('monitoring', '0078_auto_20190911_1313'), ('monitoring', '0079_auto_20190913_1747'), ('monitoring', '0080_auto_20190913_1912'), ('monitoring', '0081_auto_20190913_1918'), ('monitoring', '0082_auto_20190913_1951'), ('monitoring', '0083_auto_20190913_2015'), ('monitoring', '0084_auto_20190917_0651'), ('monitoring', '0085_projectcontact_organization'), ('monitoring', '0086_auto_20190917_1702'), ('monitoring', '0087_template'), ('monitoring', '0088_auto_20190918_0357'), ('monitoring', '0089_auto_20190918_0359'), ('monitoring', '0090_sex'), ('monitoring', '0091_auto_20190925_0721'), ('monitoring', '0092_request'), ('monitoring', '0093_auto_20191001_0657'), ('monitoring', '0094_subproject_organization'), ('monitoring', '0095_auto_20191002_1323'), ('monitoring', '0096_auto_20191007_1916'), ('monitoring', '0097_auto_20191008_1608'), ('monitoring', '0098_auto_20191008_1810'), ('monitoring', '0099_auto_20191008_1811'), ('monitoring', '0100_auto_20191011_1528'), ('monitoring', '0101_auto_20191014_0618'), ('monitoring', '0102_auto_20191014_1752'), ('monitoring', '0103_remove_contact_created_user'), ('monitoring', '0104_auto_20191014_1757'), ('monitoring', '0105_auto_20191014_1823'), ('monitoring', '0106_auto_20191017_0916'), ('monitoring', '0107_city'), ('monitoring', '0108_auto_20191017_1419'), ('monitoring', '0109_city_country'), ('monitoring', '0110_auto_20191017_1447'), ('monitoring', '0111_countryne'), ('monitoring', '0112_auto_20191017_1523'), ('monitoring', '0113_auto_20191017_1525'), ('monitoring', '0114_auto_20191017_1528'), ('monitoring', '0115_auto_20191017_1532'), ('monitoring', '0116_countryne_sov_a3'), ('monitoring', '0117_auto_20191017_1551'), ('monitoring', '0118_auto_20191017_1552'), ('monitoring', '0119_auto_20191017_1743'), ('monitoring', '0120_auto_20191017_1744'), ('monitoring', '0121_auto_20191017_1750'), ('monitoring', '0122_template_mapping'), ('monitoring', '0123_auto_20191021_1359'), ('monitoring', '0124_auto_20191023_1536')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('name_es', models.CharField(max_length=255, verbose_name='Name ES')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('codigo_numerico', models.IntegerField(verbose_name='Numerical Code')),
                ('id', models.CharField(max_length=2, primary_key=True, serialize=False, verbose_name='Id')),
                ('alfa3', models.CharField(max_length=3, verbose_name='Alfa3')),
                ('x', models.CharField(max_length=255, verbose_name='X')),
                ('y', models.CharField(max_length=255, verbose_name='Y')),
                ('subregion', models.CharField(blank=True, max_length=255, null=True, verbose_name='Sub Region')),
                ('name_fr', models.CharField(max_length=255, verbose_name='Name FR')),
                ('phonecode', models.CharField(blank=True, max_length=5, null=True, verbose_name='Phone Code')),
                ('region', models.CharField(blank=True, max_length=255, null=True, verbose_name='Region')),
            ],
            options={
                'db_table': 'country',
                'ordering': ['name'],
                'verbose_name_plural': 'Countries',
                'verbose_name': 'Country',
            },
        ),
        migrations.CreateModel(
            name='OrganizationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbreviation', models.CharField(max_length=45, verbose_name='Abbreviation')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('name_es', models.CharField(max_length=255, verbose_name='Name ES')),
                ('name_fr', models.CharField(max_length=255, verbose_name='Name FR')),
            ],
            options={
                'db_table': 'organization_type',
                'ordering': ['name'],
                'managed': False,
                'verbose_name': 'Organization Type',
                'verbose_name_plural': 'Organization Types',
            },
        ),
        migrations.CreateModel(
            name='Education',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('name_es', models.CharField(max_length=100, verbose_name='Name ES')),
                ('name_fr', models.CharField(max_length=100, verbose_name='Name FR')),
                ('varname', models.CharField(default='', max_length=100, verbose_name='Variable Id')),
                ('varname_es', models.CharField(default='', max_length=100, verbose_name='Variable Id ES')),
                ('varname_fr', models.CharField(default='', max_length=100, verbose_name='Variable Id FR')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Education',
                'verbose_name_plural': 'Educations',
            },
        ),
        migrations.CreateModel(
            name='ContactType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('name_es', models.CharField(max_length=100, verbose_name='Name ES')),
                ('name_fr', models.CharField(max_length=100, verbose_name='Name FR')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Contact Type',
                'verbose_name_plural': 'Contacts Types',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('name_es', models.CharField(max_length=100, verbose_name='Name ES')),
                ('name_fr', models.CharField(max_length=100, verbose_name='Name FR')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Country', verbose_name='Country')),
                ('organization_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.OrganizationType', verbose_name='Organization Type')),
                ('description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Description')),
                ('country_number', models.IntegerField(blank=True, null=True, verbose_name='Country Number')),
                ('is_implementer', models.BooleanField(default=False, verbose_name='Is Implementer')),
                ('organization', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='monitoring.Organization', verbose_name='Organization')),
                ('created', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('created_user', models.CharField(blank=True, max_length=20, null=True, verbose_name='Created by')),
                ('updated_user', models.CharField(blank=True, max_length=20, null=True, verbose_name='Modified by')),
            ],
            options={
                'db_table': 'organization',
                'ordering': ['name'],
                'managed': False,
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('code', models.CharField(max_length=255, verbose_name='Code')),
                ('logo', models.CharField(blank=True, max_length=255, null=True, verbose_name='Logo')),
                ('colors', models.CharField(blank=True, max_length=150, null=True, verbose_name='Colors')),
                ('url', models.URLField(blank=True, null=True, verbose_name='Url')),
                ('start', models.DateField(blank=True, null=True, verbose_name='Start')),
                ('end', models.DateField(blank=True, null=True, verbose_name='End')),
                ('countries', models.ManyToManyField(blank=True, to='monitoring.Country', verbose_name='Countries')),
                ('salesforce', models.CharField(blank=True, max_length=255, null=True, verbose_name='Salesforce Id')),
                ('targetmen', models.IntegerField(blank=True, db_column='goal_men', null=True, verbose_name='Target Men')),
                ('targetwomen', models.IntegerField(blank=True, db_column='goal_women', null=True, verbose_name='Target Women')),
            ],
            options={
                'db_table': 'project',
                'ordering': ['name'],
                'managed': False,
                'verbose_name': 'Project',
                'verbose_name_plural': 'Projects',
            },
        ),
        migrations.CreateModel(
            name='LWRRegion',
            fields=[
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('subregions', models.CharField(blank=True, max_length=200, null=True, verbose_name='Subregions')),
                ('code', models.CharField(max_length=8, primary_key=True, serialize=False, verbose_name='Id')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'LWR Region',
                'verbose_name_plural': 'LWR Regions',
            },
        ),
        migrations.AlterModelTable(
            name='lwrregion',
            table='lwrregion',
        ),
        migrations.RenameField(
            model_name='lwrregion',
            old_name='code',
            new_name='id',
        ),
        migrations.AddField(
            model_name='country',
            name='lwrregion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.LWRRegion', verbose_name='LWR Region'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'French'), ('es', 'Spanish')], default='en', max_length=2, verbose_name='Language')),
                ('countries', models.ManyToManyField(blank=True, to='monitoring.Country', verbose_name='Countries')),
                ('projects', models.ManyToManyField(blank=True, to='monitoring.Project', verbose_name='Projects')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('lwrregions', models.ManyToManyField(blank=True, to='monitoring.LWRRegion', verbose_name='LWR Regions')),
            ],
            options={
                'ordering': ['user'],
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='lwrregion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.LWRRegion', verbose_name='LWR Region'),
        ),
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.CharField(blank=True, choices=[('In Development', 'In Development'), ('Active', 'Active'), ('Inactive', 'Inactive'), ('Closed', 'Closed'), ('Suspended', 'Suspended'), ('Terminated', 'Terminated')], max_length=50, null=True, verbose_name='Status'),
        ),
        migrations.AddField(
            model_name='project',
            name='targetimen',
            field=models.IntegerField(blank=True, null=True, verbose_name='Target Indirect Men'),
        ),
        migrations.AddField(
            model_name='project',
            name='targetiwomen',
            field=models.IntegerField(blank=True, null=True, verbose_name='Target Indirect Women'),
        ),
        migrations.AlterField(
            model_name='project',
            name='targetmen',
            field=models.IntegerField(blank=True, db_column='goal_men', null=True, verbose_name='Target Direct Men'),
        ),
        migrations.AlterField(
            model_name='project',
            name='targetwomen',
            field=models.IntegerField(blank=True, db_column='goal_women', null=True, verbose_name='Target Direct Women'),
        ),
        migrations.AlterField(
            model_name='project',
            name='salesforce',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Salesforce Id'),
        ),
        migrations.AlterField(
            model_name='project',
            name='code',
            field=models.CharField(max_length=255, unique=True, verbose_name='Code'),
        ),
        migrations.AddField(
            model_name='project',
            name='recordtype',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Record Type'),
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('start', models.IntegerField(verbose_name='Start')),
                ('end', models.IntegerField(verbose_name='End')),
                ('slug', models.CharField(max_length=255, verbose_name='Slug')),
                ('order', models.IntegerField(blank=True, null=True, verbose_name='Order')),
                ('filter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='monitoring.Filter', verbose_name='Filter')),
            ],
            options={
                'db_table': 'filter',
                'ordering': ['slug', 'name'],
                'managed': False,
                'verbose_name': 'Filter',
                'verbose_name_plural': 'Filters',
            },
        ),
        migrations.CreateModel(
            name='Sex',
            fields=[
                ('id', models.CharField(max_length=1, primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('name_es', models.CharField(max_length=255, verbose_name='Name ES')),
                ('name_fr', models.CharField(max_length=255, verbose_name='Name FR')),
                ('varname', models.CharField(default='', max_length=255, verbose_name='Variable Id')),
                ('varname_es', models.CharField(default='', max_length=255, verbose_name='Variable Id ES')),
                ('varname_fr', models.CharField(default='', max_length=255, verbose_name='Variable Id FR')),
            ],
            options={
                'verbose_name': 'Sex',
                'verbose_name_plural': 'Sex',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='project',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='Modified'),
        ),
        migrations.AddField(
            model_name='project',
            name='created_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='project',
            name='updated_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Modified by'),
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.CharField(max_length=16, primary_key=True, serialize=False, verbose_name='Id')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Data Source',
                'verbose_name_plural': 'Data Sources',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('last_name', models.CharField(blank=True, max_length=80, null=True, verbose_name='Last Name')),
                ('first_name', models.CharField(blank=True, max_length=80, null=True, verbose_name='First Name')),
                ('document', models.CharField(blank=True, max_length=40, null=True, verbose_name='Document')),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Title')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Organization', verbose_name='Organization')),
                ('sex', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Sex', verbose_name='Sex')),
                ('community', models.CharField(blank=True, max_length=40, null=True, verbose_name='Community')),
                ('municipality', models.CharField(blank=True, max_length=40, null=True, verbose_name='Municipality')),
                ('city', models.CharField(blank=True, max_length=40, null=True, verbose_name='City')),
                ('country', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Country', verbose_name='Country')),
                ('phone_personal', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Personal')),
                ('phone_work', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Work')),
                ('men_home', models.IntegerField(blank=True, null=True, verbose_name='Men Home')),
                ('women_home', models.IntegerField(blank=True, null=True, verbose_name='Women Home')),
                ('created', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.ContactType', verbose_name='Type')),
                ('birthdate', models.DateField(blank=True, null=True, verbose_name='Birthdate')),
                ('education', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Education', verbose_name='Education')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('created_user', models.CharField(blank=True, max_length=20, null=True, verbose_name='Created by')),
                ('updated_user', models.CharField(blank=True, max_length=20, null=True, verbose_name='Modified by')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Source', verbose_name='Data Source')),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326, verbose_name='Location')),
            ],
            options={
                'db_table': 'contact',
                'ordering': ['name'],
                'managed': False,
                'verbose_name': 'Contact',
                'verbose_name_plural': 'Contacts',
            },
        ),
        migrations.AddField(
            model_name='organization',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Source', verbose_name='Data Source'),
        ),
        migrations.AddField(
            model_name='project',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Source', verbose_name='Data Source'),
        ),
        migrations.CreateModel(
            name='ProjectContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Product', verbose_name='Product')),
                ('area', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Area')),
                ('development_area', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Development Area')),
                ('productive_area', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Productive Area')),
                ('age_development_plantation', models.IntegerField(blank=True, null=True, verbose_name='Age Development Plantation')),
                ('age_productive_plantation', models.IntegerField(blank=True, null=True, verbose_name='Age Productive Plantation')),
                ('yield_field', models.FloatField(blank=True, db_column='yield', null=True, verbose_name='Yield Field')),
                ('date_entry_project', models.DateField(blank=True, null=True, verbose_name='Date Entry Project')),
                ('date_end_project', models.DateField(blank=True, null=True, verbose_name='Date End Project')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Contact', verbose_name='Contact')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Project', verbose_name='Project')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Organization', verbose_name='Organization')),
                ('created', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('created_user', models.CharField(blank=True, max_length=20, null=True, verbose_name='Created by')),
                ('updated_user', models.CharField(blank=True, max_length=20, null=True, verbose_name='Modified by')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Source', verbose_name='Data Source')),
            ],
            options={
                'db_table': 'project_contact',
                'ordering': ['project', 'contact'],
                'managed': False,
                'verbose_name': 'Project Contact',
                'verbose_name_plural': 'Project Contacts',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta', models.TextField()),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('created_user', models.CharField(blank=True, max_length=20, null=True, verbose_name='Created by')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Source', verbose_name='Data Source')),
            ],
        ),
        migrations.CreateModel(
            name='SubProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('code', models.CharField(max_length=255, verbose_name='Code')),
                ('salesforce', models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Salesforce Id')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Project', verbose_name='Project')),
                ('targetimen', models.IntegerField(blank=True, null=True, verbose_name='Target Indirect Men')),
                ('targetiwomen', models.IntegerField(blank=True, null=True, verbose_name='Target Indirect Women')),
                ('targetmen', models.IntegerField(blank=True, null=True, verbose_name='Target Direct Men')),
                ('targetwomen', models.IntegerField(blank=True, null=True, verbose_name='Target Direct Women')),
                ('status', models.CharField(blank=True, choices=[('Proposed', 'Proposed'), ('Active', 'Active'), ('Inactive', 'Inactive'), ('Suspended', 'Suspended'), ('Terminated', 'Terminated'), ('Closed', 'Closed')], max_length=50, null=True, verbose_name='Status')),
                ('end', models.DateField(blank=True, null=True, verbose_name='End')),
                ('start', models.DateField(blank=True, null=True, verbose_name='Start')),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Country', verbose_name='Country')),
                ('recordtype', models.CharField(blank=True, max_length=100, null=True, verbose_name='Record Type')),
                ('actualimen', models.IntegerField(blank=True, null=True, verbose_name='Actual Indirect Men')),
                ('actualiwomen', models.IntegerField(blank=True, null=True, verbose_name='Actual Indirect Women')),
                ('actualmen', models.IntegerField(blank=True, null=True, verbose_name='Actual Direct Men')),
                ('actualwomen', models.IntegerField(blank=True, null=True, verbose_name='Actual Direct Women')),
                ('organization', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Organization', verbose_name='Implementing Organization')),
                ('created', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Modified')),
                ('created_user', models.CharField(blank=True, max_length=20, null=True, verbose_name='Created by')),
                ('updated_user', models.CharField(blank=True, max_length=20, null=True, verbose_name='Modified by')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Source', verbose_name='Data Source')),
            ],
            options={
                'verbose_name': 'Sub Project',
                'verbose_name_plural': 'Sub Projects',
                'db_table': 'subproject',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
            options={
                'verbose_name_plural': 'Cities',
                'ordering': ('name',),
            },
        ),
        migrations.AlterModelTable(
            name='city',
            table='city',
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Country', verbose_name='Country'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name_es',
            field=models.CharField(max_length=255, unique=True, verbose_name='Name ES'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name_fr',
            field=models.CharField(max_length=255, unique=True, verbose_name='Name FR'),
        ),
        migrations.CreateModel(
            name='CountryNE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name')),
                ('name_es', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name ES')),
                ('name_fr', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name FR')),
                ('geometry', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('iso_a2', models.CharField(blank=True, max_length=2, null=True)),
                ('sov_a3', models.CharField(blank=True, max_length=3, null=True)),
            ],
            options={
                'db_table': 'countryne',
                'ordering': ('name',),
            },
        ),
        migrations.AlterField(
            model_name='country',
            name='codigo_numerico',
            field=models.IntegerField(blank=True, null=True, verbose_name='Numerical Code'),
        ),
        migrations.AlterField(
            model_name='country',
            name='x',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='X'),
        ),
        migrations.AlterField(
            model_name='country',
            name='y',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Y'),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set(),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.CharField(max_length=32, primary_key=True, serialize=False, verbose_name='Filename')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('file', models.FileField(blank=True, null=True, upload_to='templates/', verbose_name='File')),
                ('file_es', models.FileField(blank=True, null=True, upload_to='templates/', verbose_name='File ES')),
                ('file_fr', models.FileField(blank=True, null=True, upload_to='templates/', verbose_name='File FR')),
                ('name_es', models.CharField(max_length=50, verbose_name='Name ES')),
                ('name_fr', models.CharField(max_length=50, verbose_name='Name FR')),
                ('mapping', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Mapping')),
                ('mapping_es', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Mapping ES')),
                ('mapping_fr', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Mapping FR')),
            ],
            options={
                'verbose_name': 'Template',
                'verbose_name_plural': 'Templates',
                'db_table': 'template',
                'ordering': ['name'],
            },
        ),
    ]
