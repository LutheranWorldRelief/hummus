# Generated by Django 2.2.3 on 2019-07-25 18:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authassignment',
            options={'ordering': ['user', 'item_name']},
        ),
    ]
