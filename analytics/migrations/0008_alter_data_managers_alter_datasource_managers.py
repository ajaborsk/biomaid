# Generated by Django 4.2.7 on 2024-01-23 16:41

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0007_remove_datasource_dependencies_datasource_inputs_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='data',
            managers=[
                ('records', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='datasource',
            managers=[
                ('records', django.db.models.manager.Manager()),
            ],
        ),
    ]
