# Generated by Django 2.2.3 on 2019-07-29 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0018_auto_20190729_1822'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organizationtype',
            options={'ordering': ['name']},
        ),
    ]
