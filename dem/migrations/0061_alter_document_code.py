# Generated by Django 4.0.4 on 2022-05-07 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0060_remove_demande_soumis_a_avis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='code',
            field=models.CharField(blank=True, choices=[('DE', 'Devis'), ('CO', 'Doc commerciale'), ('CR', 'Email, courrier'), ('IM', 'Photo'), ('AS', 'Article scientifique'), ('TR', 'Texte réglementaire'), ('RE', 'Recommandations'), ('RC', 'Compte-rendu'), ('PM', 'Planning de mutualisation'), ('BP', 'Business Plan'), ('ME', 'Etude médico-économique'), ('TE', 'Doc technique'), ('DRA', "Demande de Réalisation d'Achat"), ('REF', 'Bon de demande de réforme'), ('DI', 'Autre document')], help_text='Choisissez le type du document à joindre', max_length=3, verbose_name='Type'),
        ),
    ]
