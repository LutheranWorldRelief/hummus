# Generated by Django 2.2.4 on 2019-10-17 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0120_auto_20191017_1744'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='city',
            unique_together=set(),
        ),
    ]
