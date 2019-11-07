# Generated by Django 2.2.6 on 2019-11-07 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitoring', '0011_auto_20191106_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='document',
            field=models.CharField(blank=True, db_index=True, max_length=40, null=True, verbose_name='Document'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='code',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='salesforce',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, unique=True, verbose_name='Salesforce Id'),
        ),
        migrations.AlterField(
            model_name='subproject',
            name='code',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Code'),
        ),
        migrations.AlterField(
            model_name='subproject',
            name='name',
            field=models.CharField(db_index=True, max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='subproject',
            name='salesforce',
            field=models.CharField(blank=True, db_index=True, max_length=255, null=True, unique=True, verbose_name='Salesforce Id'),
        ),
        migrations.AlterUniqueTogether(
            name='contact',
            unique_together={('name', 'first_name', 'last_name', 'document', 'country')},
        ),
        migrations.AlterUniqueTogether(
            name='projectcontact',
            unique_together={('project', 'contact')},
        ),
        migrations.AddIndex(
            model_name='contact',
            index=models.Index(fields=['first_name', 'last_name'], name='contact_first_n_af86f4_idx'),
        ),
    ]
