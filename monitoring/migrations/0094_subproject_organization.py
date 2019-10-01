# Generated by Django 2.2.4 on 2019-10-01 19:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0093_auto_20191001_0657'),
    ]

    operations = [
        migrations.AddField(
            model_name='subproject',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Organization', verbose_name='Implementing Organization'),
        ),
    ]
