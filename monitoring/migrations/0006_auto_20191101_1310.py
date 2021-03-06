# Generated by Django 2.2.6 on 2019-11-01 13:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0005_auto_20191029_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='monitoring.Log', verbose_name='Related event'),
        ),
        migrations.AddField(
            model_name='organization',
            name='log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='monitoring.Log', verbose_name='Related event'),
        ),
        migrations.AddField(
            model_name='project',
            name='log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='monitoring.Log', verbose_name='Related event'),
        ),
        migrations.AddField(
            model_name='projectcontact',
            name='log',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='monitoring.Log', verbose_name='Related event'),
        ),
    ]
