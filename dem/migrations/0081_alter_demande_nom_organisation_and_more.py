# Generated by Django 4.0 on 2022-11-01 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0080_demande_workflow_alert'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='nom_organisation',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='demande',
            name='nom_pole_court',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='demande',
            name='nom_uf_court',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
