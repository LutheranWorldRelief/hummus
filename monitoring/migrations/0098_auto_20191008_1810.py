# Generated by Django 2.2.4 on 2019-10-08 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0097_auto_20191008_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='created_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='organization',
            name='updated_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Modified by'),
        ),
        migrations.AddField(
            model_name='project',
            name='created_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='project',
            name='updated_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Modified by'),
        ),
        migrations.AddField(
            model_name='projectcontact',
            name='created_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Created by'),
        ),
        migrations.AddField(
            model_name='projectcontact',
            name='updated_user',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Modified by'),
        ),
    ]
