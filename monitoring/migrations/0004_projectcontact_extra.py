# Generated by Django 2.2.6 on 2019-10-28 15:28

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0003_auto_20191028_1429'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcontact',
            name='extra',
            field=django.contrib.postgres.fields.jsonb.JSONField(
                blank=True, null=True, verbose_name='Extra Data'),
        ),
    ]