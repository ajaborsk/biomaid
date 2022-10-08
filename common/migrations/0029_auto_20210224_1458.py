# Generated by Django 3.0.7 on 2021-02-24 13:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0028_fournisseur_nom'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataFournisseurGEF',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code_gef', models.CharField(default=None, max_length=60)),
                ('intitule_fournisseur', models.CharField(default=None, max_length=60)),
                ('raison_sociale', models.CharField(default=None, max_length=60)),
                ('adresse_1_fournisseur', models.TextField(blank=True, default=None, null=True)),
                ('cp_fournisseur', models.CharField(blank=True, default=None, max_length=25, null=True)),
                ('ville_fournisseur', models.CharField(blank=True, default=None, max_length=60, null=True)),
                ('tel_fournisseur', models.CharField(blank=True, default=None, max_length=25, null=True)),
                ('fax_fournisseur', models.CharField(blank=True, default=None, max_length=25, null=True)),
                ('telex_fournisseur', models.CharField(blank=True, default=None, max_length=25, null=True)),
                ('nu_siret', models.CharField(max_length=25)),
                ('num_tva_intracommunautaire', models.CharField(blank=True, default=None, max_length=25, null=True)),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('date_fin', models.DateField(blank=True, null=True, verbose_name='date de fin')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
            ],
        ),
        migrations.RemoveField(
            model_name='fournisseur',
            name='code_recon',
        ),
        migrations.RemoveField(
            model_name='fournisseur',
            name='etablissement',
        ),
        migrations.AddField(
            model_name='contactfournisseur',
            name='etablissement',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='common.Etablissement'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='CarnetFournisseur',
        ),
        migrations.AddField(
            model_name='datafournisseurgef',
            name='code_recon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='common.Fournisseur'),
        ),
        migrations.AddField(
            model_name='datafournisseurgef',
            name='etablissement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.Etablissement'),
        ),
    ]
