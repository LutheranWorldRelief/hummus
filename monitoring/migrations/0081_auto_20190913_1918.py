# Generated by Django 2.2.4 on 2019-09-13 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0080_auto_20190913_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='code',
            field=models.CharField(max_length=255, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='subproject',
            name='code',
            field=models.CharField(max_length=255, unique=True, verbose_name='Code'),
        ),
    ]
