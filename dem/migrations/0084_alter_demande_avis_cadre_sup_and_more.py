# Generated by Django 4.2.3 on 2023-07-19 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0083_alter_demande_date_premiere_demande'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='avis_cadre_sup',
            field=models.IntegerField(blank=True, null=True, verbose_name='Avis cadre sup'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='decision_validateur',
            field=models.IntegerField(blank=True, null=True, verbose_name='Approbation'),
        ),
    ]
