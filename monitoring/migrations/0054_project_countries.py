# Generated by Django 2.2.4 on 2019-09-06 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0053_auto_20190904_1725'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='countries',
            field=models.ManyToManyField(blank=True, to='monitoring.Country', verbose_name='Countries'),
        ),
    ]
