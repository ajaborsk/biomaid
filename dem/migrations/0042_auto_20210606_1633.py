# Generated by Django 3.2.3 on 2021-06-06 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0041_auto_20210606_1621'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_devact',
            field=models.BooleanField(default=False, help_text='TODO...', verbose_name='Augmentation des effectifs'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_normes',
            field=models.BooleanField(default=False, help_text='TODO...', verbose_name="Développement d'activité"),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_eqpt',
            field=models.BooleanField(default=False, help_text='TODO...', verbose_name="Arrivée d'un équipement"),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_qvt',
            field=models.BooleanField(default=False, help_text='TODO...', verbose_name='Qualité de Vie au Travail'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_reorg',
            field=models.BooleanField(default=False, help_text='TODO...', verbose_name='Réorganisation des activités'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_securite',
            field=models.BooleanField(default=False, help_text='TODO...', verbose_name='Sécurité des patients'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='tvx_arg_vetustes',
            field=models.BooleanField(default=False, help_text='TODO...', verbose_name='Locaux vétustes'),
        ),
    ]
