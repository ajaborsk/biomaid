# Generated by Django 3.2.3 on 2021-08-10 05:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0047_alter_calendrier_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='demande',
            old_name='montant',
            new_name='montant_bak',
        ),
        migrations.RenameField(
            model_name='demande',
            old_name='montant_total_expert_metier',
            new_name='montant_total_expert_metier_bak',
        ),
    ]
