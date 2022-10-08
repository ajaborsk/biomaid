# Generated by Django 3.0.7 on 2020-10-06 19:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0019_auto_20201006_2140'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0009_acheteur_discipline_domaine_programme'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Acheteur',
            new_name='ExpertMetier',
        ),
        migrations.RenameField(
            model_name='domaine',
            old_name='acheteur',
            new_name='expert_metier',
        ),
        migrations.AlterField(
            model_name='userufrole',
            name='role_code',
            field=models.CharField(
                choices=[
                    ('CHP', 'Chef de pôle'),
                    ('ADCP', 'Adjoint au chef de pôle'),
                    ('CHS', 'Chef de service'),
                    ('RUN', "Responsable d'unité"),
                    ('CSP', 'Cadre supérieur de pôle'),
                    ('DRP', 'Directeur référent de pôle'),
                    ('CAP', 'Cadre administratif de pôle'),
                    ('AMAR', 'Assistant médico-administratif référent'),
                    ('CADS', 'Cadre supérieur'),
                    ('CAD', 'Cadre'),
                    ('COP', 'Coordonateur de pôle'),
                    ('DIR', 'Directeur adjoint'),
                    ('RMA', 'Référent matériel'),
                    ('ACH', 'Acheteur'),
                    ('EXP', 'Expertmetier'),
                ],
                max_length=5,
            ),
        ),
    ]
