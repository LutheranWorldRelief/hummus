# Generated by Django 2.2.4 on 2019-10-17 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0109_city_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=255, unique=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name_es',
            field=models.CharField(max_length=255, unique=True, verbose_name='Name ES'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name_fr',
            field=models.CharField(max_length=255, unique=True, verbose_name='Name FR'),
        ),
    ]
