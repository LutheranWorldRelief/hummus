# Generated by Django 2.2.6 on 2019-11-01 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0009_auto_20191101_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='status',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Status'),
        ),
    ]
