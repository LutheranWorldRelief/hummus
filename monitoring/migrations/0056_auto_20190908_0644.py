# Generated by Django 2.2.4 on 2019-09-08 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0055_auto_20190906_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='continent',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Continent'),
        ),
        migrations.AddField(
            model_name='country',
            name='subregion',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Sub Region'),
        ),
    ]
