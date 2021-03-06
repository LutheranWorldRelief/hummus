# Generated by Django 2.2.4 on 2019-09-09 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0062_subproject'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Region',
            new_name='LWRRegion',
        ),
        migrations.AlterModelOptions(
            name='lwrregion',
            options={'ordering': ['name'], 'verbose_name': 'LWR Region', 'verbose_name_plural': 'LWR Regions'},
        ),
        migrations.AlterModelOptions(
            name='organizationtype',
            options={'ordering': ['name'], 'verbose_name': 'Organization Type', 'verbose_name_plural': 'Organization Types'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['name'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='projectcontact',
            options={'ordering': ['project', 'contact'], 'verbose_name': 'Project Contact', 'verbose_name_plural': 'Project Contacts'},
        ),
        migrations.RemoveField(
            model_name='country',
            name='region',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='regiones',
        ),
        migrations.AddField(
            model_name='country',
            name='lwrregion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.LWRRegion', verbose_name='LWR Region'),
        ),
        migrations.AddField(
            model_name='profile',
            name='regions',
            field=models.ManyToManyField(blank=True, to='monitoring.LWRRegion', verbose_name='LWR Regions'),
        ),
    ]
