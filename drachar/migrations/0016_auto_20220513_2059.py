# Generated by Django 3.2.11 on 2022-05-13 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drachar', '0015_auto_20220210_0659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactlivraison',
            old_name='date_fin',
            new_name='cloture',
        ),
        migrations.RenameField(
            model_name='dossier',
            old_name='date_fin',
            new_name='cloture',
        ),
    ]
