# Generated by Django 3.0.7 on 2020-10-11 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0019_auto_20201006_2140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demande',
            old_name='montant_expertmetier_total',
            new_name='montant_total_expert_metier',
        ),
    ]
