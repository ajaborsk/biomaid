# Generated by Django 3.0.7 on 2020-10-26 06:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0023_auto_20201022_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='demande',
            name='state_code',
            field=models.CharField(blank=True, default=None, max_length=16, null=True, verbose_name='Etat de la demande'),
        ),
    ]
