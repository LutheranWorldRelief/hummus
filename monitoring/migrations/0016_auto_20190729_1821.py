# Generated by Django 2.2.3 on 2019-07-29 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0015_auto_20190729_1820'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['name']},
        ),
    ]
