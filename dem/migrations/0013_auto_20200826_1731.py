# Generated by Django 3.0.7 on 2020-08-26 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0012_auto_20200824_0634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='decision_validateur',
            field=models.BooleanField(null=True, verbose_name='Décision'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='enveloppe_allouee',
            field=models.DecimalField(
                blank=True,
                decimal_places=0,
                default=None,
                help_text='enveloppe financière allouée par la commission',
                max_digits=9,
                null=True,
                verbose_name="montant de l'enveloppe allouée",
            ),
        ),
        migrations.AlterField(
            model_name='demande',
            name='montant_acheteur_total',
            field=models.DecimalField(
                blank=True,
                decimal_places=0,
                default=None,
                help_text="Montant Total estimé par l'acheteur en fonction du projet et des quantités souhaitées",
                max_digits=9,
                null=True,
                verbose_name="Montant Total estimé par l'acheteur",
            ),
        ),
        migrations.AlterField(
            model_name='demande',
            name='montant_unitaire_acheteur',
            field=models.DecimalField(
                blank=True,
                decimal_places=0,
                default=None,
                help_text="Montant unitaire estimé par l'acheteur en fonction du projet",
                max_digits=9,
                null=True,
                verbose_name="Montant unitaire estimé par l'acheteur",
            ),
        ),
    ]
