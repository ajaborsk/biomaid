# Generated by Django 4.0 on 2022-11-06 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0081_alter_demande_nom_organisation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demande',
            name='state_code',
        ),
    ]
