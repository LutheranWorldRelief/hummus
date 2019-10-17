# Generated by Django 2.2.4 on 2019-10-17 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0111_countryne'),
    ]

    operations = [
        migrations.AddField(
            model_name='countryne',
            name='iso_a2',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='countryne',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='countryne',
            name='name_es',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Name ES'),
        ),
        migrations.AlterField(
            model_name='countryne',
            name='name_fr',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Name FR'),
        ),
    ]
