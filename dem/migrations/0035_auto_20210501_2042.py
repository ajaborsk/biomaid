# Generated by Django 3.1.4 on 2021-05-01 18:42

import dem.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0034_demande_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='code',
            field=models.CharField(default=dem.models.increment_code_number, max_length=400),
        ),
        migrations.AlterField(
            model_name='demande',
            name='date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Date de la demande'),
        ),
    ]
