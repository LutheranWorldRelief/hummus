# Generated by Django 2.2.8 on 2019-12-12 06:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0017_auto_20191120_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiaries',
            fields=[
                ('id', models.AutoField(auto_created=True,
                                        primary_key=True, serialize=False, verbose_name='ID')),
                ('salesforce', models.CharField(blank=True, max_length=255,
                                                null=True, unique=True, verbose_name='Salesforce Id')),
                ('fiscalyear', models.IntegerField(verbose_name='Fiscal Year')),
                ('quarter', models.IntegerField(verbose_name='Quarter')),
                ('actualmen', models.IntegerField(blank=True, null=True, verbose_name='Actual Direct Men')),
                ('actualwomen', models.IntegerField(blank=True,
                                                    null=True, verbose_name='Actual Direct Women')),
                ('actualimen', models.IntegerField(blank=True,
                                                   null=True, verbose_name='Actual Indirect Men')),
                ('actualiwomen', models.IntegerField(blank=True,
                                                     null=True, verbose_name='Actual Indirect Women')),
                ('targetmen', models.IntegerField(blank=True, null=True, verbose_name='Target Direct Men')),
                ('targetwomen', models.IntegerField(blank=True,
                                                    null=True, verbose_name='Target Direct Women')),
                ('targetimen', models.IntegerField(blank=True,
                                                   null=True, verbose_name='Target Indirect Men')),
                ('targetiwomen', models.IntegerField(blank=True,
                                                     null=True, verbose_name='Target Indirect Women')),
                ('subproject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                 to='monitoring.SubProject', verbose_name='Sub Project')),
            ],
            options={
                'ordering': ['fiscalyear', 'quarter', 'subproject'],
            },
        ),
    ]