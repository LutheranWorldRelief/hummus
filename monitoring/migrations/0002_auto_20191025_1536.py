# Generated by Django 2.2.6 on 2019-10-25 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0001_squashed_0124_auto_20191023_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='education',
            name='varname',
            field=models.CharField(max_length=100, verbose_name='Variable Id'),
        ),
        migrations.AlterField(
            model_name='education',
            name='varname_es',
            field=models.CharField(max_length=100, verbose_name='Variable Id ES'),
        ),
        migrations.AlterField(
            model_name='education',
            name='varname_fr',
            field=models.CharField(max_length=100, verbose_name='Variable Id FR'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='projectcontact',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
        migrations.AlterField(
            model_name='sex',
            name='varname',
            field=models.CharField(max_length=255, verbose_name='Variable Id'),
        ),
        migrations.AlterField(
            model_name='sex',
            name='varname_es',
            field=models.CharField(max_length=255, verbose_name='Variable Id ES'),
        ),
        migrations.AlterField(
            model_name='sex',
            name='varname_fr',
            field=models.CharField(max_length=255, verbose_name='Variable Id FR'),
        ),
        migrations.AlterField(
            model_name='subproject',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Created'),
        ),
    ]
