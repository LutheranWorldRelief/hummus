# Generated by Django 2.2.3 on 2019-08-12 14:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0040_auto_20190801_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='organization_type_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='monitoring.OrganizationType'),
        ),
    ]
