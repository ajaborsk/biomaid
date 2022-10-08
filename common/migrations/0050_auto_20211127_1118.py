# Generated by Django 3.2.4 on 2021-11-27 10:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0049_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AddField(
            model_name='user',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='date de création'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='date_modification',
            field=models.DateTimeField(auto_now=True, verbose_name='date de modification'),
        ),
        migrations.AddField(
            model_name='user',
            name='etablissement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='common.etablissement'),
        ),
        migrations.AddField(
            model_name='user',
            name='initiales',
            field=models.CharField(blank=True, max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='intitule_fonction',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='Fonction (intitulé)'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_seen',
            field=models.DateTimeField(blank=True, help_text='Date de la dernière visite sur le portail', null=True, verbose_name='Dernière visite'),
        ),
        migrations.AddField(
            model_name='user',
            name='preferences',
            field=models.TextField(default='{}', help_text="Préférences de l'utilisateur, stockées sous forme d'une chaine JSON", verbose_name='Préférences'),
        ),
        migrations.AddField(
            model_name='user',
            name='tel_dect',
            field=models.CharField(blank=True, max_length=17, verbose_name='Tél. DECT'),
        ),
        migrations.AddField(
            model_name='user',
            name='tel_fixe',
            field=models.CharField(blank=True, max_length=17, verbose_name='Tél. fixe'),
        ),
        migrations.AddField(
            model_name='user',
            name='tel_mobile',
            field=models.CharField(blank=True, max_length=17, verbose_name='Tél. mobile'),
        ),
        migrations.AddField(
            model_name='user',
            name='titre',
            field=models.CharField(blank=True, help_text='M. / Mme / Mlle / Dr / Pr ...', max_length=32, null=True, verbose_name='Titre'),
        ),
    ]
