# Generated by Django 2.2.4 on 2019-10-08 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0098_auto_20191008_1810'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='created_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='contact',
            name='updated_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Modified by'),
        ),
        migrations.AddField(
            model_name='request',
            name='created_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='subproject',
            name='created_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='subproject',
            name='updated_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Modified by'),
        ),
    ]
