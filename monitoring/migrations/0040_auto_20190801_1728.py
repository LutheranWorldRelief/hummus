# Generated by Django 2.2.3 on 2019-08-01 17:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0039_auto_20190801_1727'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='implementing_organization_id',
            new_name='organization',
        ),
    ]
