# Generated by Django 3.2.11 on 2022-05-13 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marche', '0004_auto_20210615_2157'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lot',
            old_name='date_fin',
            new_name='cloture',
        ),
        migrations.RenameField(
            model_name='marche',
            old_name='date_fin',
            new_name='cloture',
        ),
    ]
