# Generated by Django 4.0 on 2022-08-21 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0005_remove_datasource_auto_datasource_auto2'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datasource',
            old_name='auto2',
            new_name='auto',
        ),
    ]
