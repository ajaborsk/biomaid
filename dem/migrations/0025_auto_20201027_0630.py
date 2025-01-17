# Generated by Django 3.0.7 on 2020-10-27 05:30

import dem.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0024_demande_state_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='state_code',
            field=dem.models.DemandeStateCodeField(
                blank=True, default=None, max_length=16, null=True, verbose_name='Etat de la demande'
            ),
        ),
    ]
