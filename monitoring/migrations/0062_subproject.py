# Generated by Django 2.2.4 on 2019-09-09 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0061_project_salesforce'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('code', models.CharField(max_length=255, verbose_name='Code')),
                ('salesforce', models.CharField(blank=True, max_length=255, null=True, verbose_name='Salesforce Id')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitoring.Project', verbose_name='Project')),
            ],
            options={
                'verbose_name': 'Sub Project',
                'verbose_name_plural': 'Sub Projects',
                'db_table': 'subproject',
                'ordering': ['name'],
            },
        ),
    ]
