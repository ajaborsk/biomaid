# Generated by Django 3.1.4 on 2021-04-04 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0030_alert'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='historique',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
