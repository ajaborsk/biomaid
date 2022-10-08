#  Copyright (c)

#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

from django.db import migrations


def transfert_argumentation_detaillee(apps, schema_editor):
    model = apps.get_model('dem', 'Demande')
    records = model.objects.all()
    for record in records:
        detail_qs = apps.get_model('dem', 'ArgumentaireDetaille').objects.filter(demande=record.num_dmd)
        if detail_qs.exists():
            detail = detail_qs[0]
            record.arg_interet_medical = detail.interet_medical
            record.arg_commentaire_im = detail.commentaire_im
            record.arg_oblig_reglementaire = detail.oblig_reglementaire
            record.arg_commentaire_or = detail.commentaire_or
            record.arg_recommandations = detail.recommandations
            record.arg_commentaire_r = detail.commentaire_r
            record.arg_projet_chu_pole = detail.projet_chu_pole
            record.arg_commentaire_pcp = detail.commentaire_pcp
            record.arg_confort_patient = detail.confort_patient
            record.arg_commentaire_cp = detail.commentaire_cp
            record.arg_confort_perso_ergo = detail.confort_perso_ergo
            record.arg_commentaire_pe = detail.commentaire_pe
            record.arg_notoriete = detail.notoriete
            record.arg_commentaire_n = detail.commentaire_n
            record.arg_innovation_recherche = detail.innovation_recherche
            record.arg_commentaire_ir = detail.commentaire_ir
            record.arg_mutualisation = detail.mutualisation
            record.arg_commentaire_m = detail.commentaire_m
            record.arg_gain_financier = detail.gain_financier
            record.arg_commentaire_gf = detail.commentaire_gf
            record.save(
                update_fields=[
                    'arg_interet_medical',
                    'arg_commentaire_im',
                    'arg_oblig_reglementaire',
                    'arg_commentaire_or',
                    'arg_recommandations',
                    'arg_commentaire_r',
                    'arg_projet_chu_pole',
                    'arg_commentaire_pcp',
                    'arg_confort_patient',
                    'arg_commentaire_cp',
                    'arg_confort_perso_ergo',
                    'arg_commentaire_pe',
                    'arg_notoriete',
                    'arg_commentaire_n',
                    'arg_innovation_recherche',
                    'arg_commentaire_ir',
                    'arg_mutualisation',
                    'arg_commentaire_m',
                    'arg_gain_financier',
                    'arg_commentaire_gf',
                ]
            )


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0067_demande_arg_commentaire_cp_and_more'),
    ]

    operations = [
        migrations.RunPython(transfert_argumentation_detaillee),
    ]
