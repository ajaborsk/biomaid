# Generated by Django 3.2.3 on 2021-06-06 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0040_alter_demande_tvx_etage'),
    ]

    operations = [
        migrations.AddField(
            model_name='demande',
            name='tvx_contrainte_lar',
            field=models.BooleanField(default=False, help_text='TODO...', verbose_name='Locaux à risque'),
        ),
        migrations.AddField(
            model_name='demande',
            name='tvx_contrainte_lib',
            field=models.BooleanField(default=False, help_text='TODO...', verbose_name='Libération des locaux'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_contrainte',
            field=models.TextField(
                blank=True, help_text='TODO...', null=True, verbose_name='Autre contrainte travaux dans cette zone'
            ),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_priorite',
            field=models.CharField(
                blank=True,
                choices=[
                    ('1', 'Locaux particulièrement vétustes, travaux indispensables'),
                    ('2', "Nécessite des aménagements,  à l'origine de probleme d'exploitation"),
                    ('3', 'Amélioration significative des locaux ou du fonctionnement'),
                    ('4', 'Axe de progrès'),
                ],
                help_text='TODO...',
                max_length=8,
                null=True,
                verbose_name='Priorité',
            ),
        ),
    ]
