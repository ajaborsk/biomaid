# Generated by Django 3.2.3 on 2021-06-12 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0042_auto_20210606_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_devact',
            field=models.BooleanField(default=False, verbose_name='Augmentation des effectifs'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_devact_comment',
            field=models.TextField(blank=True, null=True, verbose_name='Augmentation des effectifs'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_normes',
            field=models.BooleanField(default=False, verbose_name="Développement d'activité"),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_normes_comment',
            field=models.TextField(blank=True, null=True, verbose_name="Développement d'activité"),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_eqpt',
            field=models.BooleanField(default=False, verbose_name="Arrivée d'un équipement"),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_eqpt_comment',
            field=models.TextField(blank=True, null=True, verbose_name="Arrivée d'un équipement"),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_qvt',
            field=models.BooleanField(default=False, verbose_name='Qualité de Vie au Travail'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_qvt_comment',
            field=models.TextField(blank=True, null=True, verbose_name='Qualité de Vie au Travail'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_reorg',
            field=models.BooleanField(default=False, verbose_name='Réorganisation des activités'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_reorg_comment',
            field=models.TextField(blank=True, null=True, verbose_name='Réorganisation des activités'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_securite',
            field=models.BooleanField(default=False, verbose_name='Sécurité des patients'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_securite_comment',
            field=models.TextField(blank=True, null=True, verbose_name='Sécurité des patients'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_vetustes',
            field=models.BooleanField(default=False, verbose_name='Locaux vétustes'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_vetustes_comment',
            field=models.TextField(blank=True, null=True, verbose_name='Locaux vétustes'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_batiment',
            field=models.CharField(
                blank=True,
                choices=[
                    ('NCHU', 'Nouveau CHU (Halls 1 et 2)'),
                    ('H3', 'Bâtiment Fontenoy (Halls 3)'),
                    ('SVP', 'Saint-Vincent de Paul'),
                    ('SV', 'Saint-Victor'),
                    ('HN', 'Hôpital Nord'),
                    ('EC', 'Ecoles'),
                    ('SIM', 'SimUSanté'),
                    ('TEP', 'TEP'),
                    ('CBH', 'CBH'),
                    ('HEM', 'Hémato'),
                    ('BB', 'Biobanque'),
                    ('AU', 'Autre'),
                ],
                max_length=8,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_contrainte',
            field=models.TextField(blank=True, null=True, verbose_name='Autre contrainte travaux dans cette zone'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_contrainte_lar',
            field=models.BooleanField(default=False, verbose_name='Locaux à risque'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_contrainte_lib',
            field=models.BooleanField(default=False, verbose_name='Libération des locaux'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_eval_confort',
            field=models.IntegerField(blank=True, null=True, verbose_name='Evaluation confort patients/personnel'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_eval_contin',
            field=models.IntegerField(blank=True, null=True, verbose_name='Evaluation continuité exploitation'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_eval_devact',
            field=models.IntegerField(blank=True, null=True, verbose_name="Evaluation développement d'activité"),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_eval_qvt',
            field=models.IntegerField(blank=True, null=True, verbose_name='Evaluation QVT'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_eval_securite',
            field=models.IntegerField(blank=True, null=True, verbose_name='Evaluation sécurité'),
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
                max_length=8,
                null=True,
                verbose_name='Priorité',
            ),
        ),
    ]
