# Generated by Django 2.2.4 on 2019-08-15 05:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0044_auto_20190812_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='organization_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Organization'),
        ),
    ]
