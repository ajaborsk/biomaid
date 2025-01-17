# Generated by Django 4.2.3 on 2023-08-22 06:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('common', '0084_programme_site'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='centreresponsabilite',
            name='etablissement',
            field=models.ForeignKey(
                blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.etablissement'
            ),
        ),
        migrations.AlterField(
            model_name='genericrole',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='pole',
            name='etablissement',
            field=models.ForeignKey(
                blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.etablissement'
            ),
        ),
        migrations.AlterField(
            model_name='service',
            name='etablissement',
            field=models.ForeignKey(
                blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.etablissement'
            ),
        ),
        migrations.AlterField(
            model_name='site',
            name='etablissement',
            field=models.ForeignKey(
                blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.etablissement'
            ),
        ),
        migrations.AlterField(
            model_name='uf',
            name='centre_responsabilite',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.centreresponsabilite'),
        ),
        migrations.AlterField(
            model_name='uf',
            name='etablissement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.etablissement'),
        ),
        migrations.AlterField(
            model_name='uf',
            name='pole',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.pole'),
        ),
        migrations.AlterField(
            model_name='uf',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.site'),
        ),
        migrations.AlterField(
            model_name='userufrole',
            name='centre_responsabilite',
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.centreresponsabilite'
            ),
        ),
        migrations.AlterField(
            model_name='userufrole',
            name='discipline',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.discipline'),
        ),
        migrations.AlterField(
            model_name='userufrole',
            name='etablissement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.etablissement'),
        ),
        migrations.AlterField(
            model_name='userufrole',
            name='pole',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.pole'),
        ),
        migrations.AlterField(
            model_name='userufrole',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.service'),
        ),
        migrations.AlterField(
            model_name='userufrole',
            name='site',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.site'),
        ),
        migrations.AlterField(
            model_name='userufrole',
            name='uf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='common.uf'),
        ),
    ]
