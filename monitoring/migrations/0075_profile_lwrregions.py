# Generated by Django 2.2.4 on 2019-09-09 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0074_remove_profile_lwrregions'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='lwrregions',
            field=models.ManyToManyField(blank=True, to='monitoring.LWRRegion', verbose_name='LWR Regions'),
        ),
    ]
