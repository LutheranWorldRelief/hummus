# Generated by Django 2.2.4 on 2019-10-17 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0116_countryne_sov_a3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='codigo_numerico',
            field=models.IntegerField(blank=True, null=True, verbose_name='Numerical Code'),
        ),
    ]
