# Generated by Django 4.0 on 2022-11-06 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0077_rename_desactivation_datetime_genericrole_cloture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericrole',
            name='role_code',
            field=models.CharField(choices=[('CHP', 'Chef de pôle'), ('ADCP', 'Adjoint au chef de pôle'), ('CHS', 'Chef de service'), ('RUN', "Responsable d'unité"), ('CSP', 'Cadre supérieur de pôle'), ('DRP', 'Directeur référent de pôle'), ('CAP', 'Cadre administratif de pôle'), ('AMAR', 'Assistant médico-administratif référent'), ('CADS', 'Cadre supérieur'), ('CAD', 'Cadre'), ('COP', 'Coordonateur de pôle'), ('DIR', 'Directeur adjoint'), ('RMA', 'Référent matériel'), ('ACH', 'Acheteur'), ('EXP', 'Expert métier'), ('RESPD', 'Responsable de domaine technique'), ('INGTX', 'Ingénieur travaux'), ('GES', 'Gestionnaire'), ('TECH', 'Technicien'), ('ADM', 'Administrateur'), ('OWN', 'Propriétaire'), ('MAN', 'Manager'), ('ARB', 'Arbitre'), ('DIS', 'Aiguilleur')], max_length=8),
        ),
    ]
