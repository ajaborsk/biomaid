# Generated by Django 4.0 on 2022-12-24 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drachar', '0032_previsionnel_valeur_inventaire_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='previsionnel',
            name='nombre_equipements',
            field=models.IntegerField(blank=True, default=None, help_text='Montant total des équipements inventoriés sur cette ligne de prévisionnel (détecté automatiquement)', null=True, verbose_name='Nombre équipements'),
        ),
    ]
