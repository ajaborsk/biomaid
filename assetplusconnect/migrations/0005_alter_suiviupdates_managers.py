# Generated by Django 4.2.7 on 2024-01-23 16:41

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('assetplusconnect', '0004_fournis2'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='suiviupdates',
            managers=[
                ('records', django.db.models.manager.Manager()),
            ],
        ),
    ]