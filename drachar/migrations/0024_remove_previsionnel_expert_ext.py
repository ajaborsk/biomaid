#  Copyright (c)

# Generated by Django 4.0.4 on 2022-05-21 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drachar', '0023_transfert_previsionnel_expert_ext'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='previsionnel',
            name='expert_ext',
        ),
    ]
