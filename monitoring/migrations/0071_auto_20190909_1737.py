# Generated by Django 2.2.4 on 2019-09-09 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0070_auto_20190909_1720'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lwrregion',
            old_name='code',
            new_name='id',
        ),
        migrations.AlterField(
            model_name='country',
            name='lwrregion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.LWRRegion', to_field='id', verbose_name='LWR Region'),
        ),
    ]
