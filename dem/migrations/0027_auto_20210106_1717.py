# Generated by Django 3.0.7 on 2021-01-06 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0026_auto_20201210_1159'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='calendrier',
            options={'verbose_name': 'campagne recensement demandes', 'verbose_name_plural': 'campagne recensement demandes'},
        ),
        migrations.AlterField(
            model_name='demande',
            name='date',
            field=models.DateField(blank=True, default='2021-01-01', null=True, verbose_name='Année de la demande'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='date_premiere_demande',
            field=models.DateField(
                blank=True,
                default='2021-01-01',
                help_text="Année où la demande a été présentée la première fois à la Commission d'arbitrage",
                null=True,
                verbose_name='Première demande',
            ),
        ),
    ]
