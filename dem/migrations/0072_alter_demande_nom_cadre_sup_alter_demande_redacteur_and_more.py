#  Copyright (c) 2020 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
#  This file is part of the BiomAid distribution.
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
# Generated by Django 4.0.5 on 2022-07-02 19:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

def cleanup_validateur(apps, schema_editor):
    model = apps.get_model('dem', 'Demande')
    records = model.objects.filter(validateur__isnull=False)
    for record in records:
        record.validateur = None
        record.save(update_fields = ['validateur'])


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dem', '0071_alter_demande_arg_commentaire_cp_and_more'),
    ]

    operations = [
        migrations.RunPython(
            cleanup_validateur
        ),
        migrations.AlterField(
            model_name='demande',
            name='nom_cadre_sup',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demandes_avis_donne', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='demande',
            name='redacteur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Rédacteur'),
        ),
        migrations.AlterField(
            model_name='demande',
            name='validateur',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='demandes_approuvees', to=settings.AUTH_USER_MODEL),
        ),
    ]
