# Generated by Django 2.2.3 on 2019-07-25 19:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legacy', '0008_auto_20190725_1859'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='authitemchild',
            unique_together=set(),
        ),
    ]
