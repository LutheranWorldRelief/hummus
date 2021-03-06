# Generated by Django 2.2.4 on 2019-09-04 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0052_auto_20190904_0321'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendance',
            options={'ordering': ['event', 'contact'], 'verbose_name': 'Attendance', 'verbose_name_plural': 'Attendances'},
        ),
        migrations.AlterModelOptions(
            name='contacttype',
            options={'ordering': ['name'], 'verbose_name': 'Contact Type', 'verbose_name_plural': 'Contacts Types'},
        ),
        migrations.AlterModelOptions(
            name='education',
            options={'ordering': ['name'], 'verbose_name': 'Education', 'verbose_name_plural': 'Educations'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['name'], 'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='filter',
            options={'ordering': ['slug', 'name'], 'verbose_name': 'Filter', 'verbose_name_plural': 'Filters'},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name'], 'verbose_name': 'Organization', 'verbose_name_plural': 'Organizations'},
        ),
        migrations.AlterModelOptions(
            name='organizationtype',
            options={'ordering': ['name'], 'verbose_name': 'Organization Type', 'verbose_name_plural': 'Organizations Types'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'verbose_name': 'Product', 'verbose_name_plural': 'products'},
        ),
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['user'], 'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['name'], 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterModelOptions(
            name='projectcontact',
            options={'ordering': ['project', 'contact'], 'verbose_name': 'Project Contact', 'verbose_name_plural': 'Projects Contacts'},
        ),
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ['name'], 'verbose_name': 'Region', 'verbose_name_plural': 'Regions'},
        ),
        migrations.AddField(
            model_name='organizationtype',
            name='name_es',
            field=models.CharField(default=1, max_length=255, verbose_name='Name_Es'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organizationtype',
            name='name_fr',
            field=models.CharField(default=1, max_length=255, verbose_name='Name_Fr'),
            preserve_default=False,
        ),
    ]
