# Generated by Django 2.2.6 on 2019-11-01 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0007_auto_20191101_1646'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='country_number',
        ),
        migrations.AddField(
            model_name='organization',
            name='varname',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Acronym'),
        ),
        migrations.RenameField(
            model_name='contact',
            old_name='type',
            new_name='contact_type',
        ),
    ]
