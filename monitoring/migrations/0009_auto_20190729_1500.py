# Generated by Django 2.2.3 on 2019-07-29 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0008_auto_20190729_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.Country'),
        ),
    ]
