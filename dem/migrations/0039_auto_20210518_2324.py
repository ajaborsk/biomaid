# Generated by Django 3.1.4 on 2021-05-18 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0038_demande_discipline_dmd'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_devact',
            field=models.BooleanField(
                blank=True, default=False, help_text='TODO...', null=True, verbose_name='Augmentation des effectifs'
            ),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_normes',
            field=models.BooleanField(
                blank=True, default=False, help_text='TODO...', null=True, verbose_name="Développement d'activité"
            ),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_eqpt',
            field=models.BooleanField(
                blank=True, default=False, help_text='TODO...', null=True, verbose_name="Arrivée d'un équipement"
            ),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_qvt',
            field=models.BooleanField(
                blank=True, default=False, help_text='TODO...', null=True, verbose_name='Qualité de Vie au Travail'
            ),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_reorg',
            field=models.BooleanField(
                blank=True, default=False, help_text='TODO...', null=True, verbose_name='Réorganisation des activités'
            ),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_securite',
            field=models.BooleanField(
                blank=True, default=False, help_text='TODO...', null=True, verbose_name='Sécurité des patients'
            ),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_vetustes',
            field=models.BooleanField(blank=True, default=False, help_text='TODO...', null=True, verbose_name='Locaux vétustes'),
        ),
    ]
