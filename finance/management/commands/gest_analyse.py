#
# This file is part of the BIOM_AID distribution (https://bitbucket.org/kig13/dem/).
# Copyright (c) 2020-2021 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
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
from django.apps import apps
from django.core.management.base import BaseCommand
from django.db import DatabaseError
from django.utils.translation import gettext as _

from finance.analytics import AllCmdChecker

ORDER_ANOMALIES = {
    # Par ligne de commande :
    # -----------------------
    '4L00': {
        'label': _("Ligne avec montant à 0 €"),
    },
    '4L01': {
        'label': _("Ligne avec montant > 0 €, dont le libellé ne comporte pas 'frais de' et non rapprochée d'une intervention"),
    },
    # Par lien ligne de commande / intervention (localisation du problème inconnue) :
    # -------------------------------------------------------------------------------
    '2L11': {
        'label': _("Non correspondance de l'UF"),
        'help_text': _("L'UF renseignée sur la ligne de commande et sur l'intervention associée sont différentes."),
    },
    '2L12': {
        'label': _("Non correspondance du N° d'inventaire"),
    },
    '2L13': {
        'label': "Non correspondance du N° de série",
    },
    # Par ligne de commande attachée à une intervention :
    # ---------------------------------------------------
    '3L01': {
        'label': "Intervention archivée et ligne non soldée",
    },
    # Par intervention liée à la commande :
    # -------------------------------------
    '4I01': {
        'label': "Intervention non rapprochée d'une ligne de commande",
    },
    '2I02': {
        'label': "Intervention ne spécifie pas le numéro de commande",
    },
    '4I03': {
        'label': "Intervention spécifie un numéro de commande différent",
    },
    # Par intervention attachée à une ligne :
    # ---------------------------------------
    # Par commande (globalement) :
    # ----------------------------
    '4C01': {
        'label': "Montant total à 0 €",
    },
    '4C02': {
        'label': "Aucune intervention rapprochée",
    },
    '3C03': {
        'label': "Au moins une ligne pourrait être soldée",
    },
    '4C03': {
        'label': "Des interventions liées ne peuvent pas être rapprochées à des lignes",
    },
    '1C01': {
        'label': "Age > 6 mois",
    },
}


class Command(BaseCommand):
    help = """Analyse de l'état des commandes"""

    def handle(self, *args, **options):
        try:
            gests = ['IF', 'II', 'IM']
            # order_anomalies = []
            ext_commande_model = apps.get_model('extable', 'ExtCommande')

            if options['verbosity'] > 1:
                self.stdout.write("Gest_analyse...")
            AllCmdChecker(ext_commande_model, gestionnaires=gests).check(verbosity=options['verbosity'])

            # order_qs = (
            #     ext_commande_model.records.filter(gest_ec__in=gests, lg_soldee_lc='N')
            #     .order_by()
            #     .annotate(lg_zero=Case(When(mt_engage_lc__gt=-0.01,
            #           mt_engage_lc__lt=0.01, then=Value(1))), default=Value(0))
            #     .annotate(lg_soldee=Case(When(lg_soldee_lc='O', lg_zero=0, then=Value(1))), default=Value(0))
            #     .values(
            #         'commande', 'date_passation_ec', 'no_fournisseur_fr',
            #         'intitule_fournisseur_fr', 'objet_depense_ec', 'bloc_note'
            #     )
            #     .annotate(
            #         lignes=Count('no_ligne_lc'),
            #         engage=Sum('mt_engage_lc'),
            #         liquide=Sum('mt_liquide_lc'),
            #         lgs_zero=Sum('lg_zero'),
            #         lgs_soldees=Sum('lg_soldee'),
            #     )
            #     .distinct()
            #     .order_by('date_passation_ec')
            # )
            #
            # print(f"Commandes avec des lignes non soldées : {order_qs.count()}")
            # lc_count = 0
            # for order in order_qs:
            #     order_rows = ext_commande_model.records.filter(commande=order['commande']).order_by('no_ligne_lc')
            #
            #     rows = [
            #         dict(row, **{'interv': no_interv_re.findall(row['libelle'])})
            #         for row in order_rows.values(
            #             'no_ligne_lc',
            #             'libelle',
            #             'mt_engage_lc',
            #             'lg_soldee_lc',
            #             'commande',
            #             'no_uf_uf',
            #         )
            #     ]
            #     intvs = get_intv_from_order(order, rows)
            #     matcher = IntvLignesRecordMatcher({row['no_ligne_lc']: row for row in rows}, intvs)
            #     matches = matcher.get_all_results()
            #
            #     # print([len(t) for t in matcher.get_all_results()])
            #     for order_row in order_rows:
            #
            #         order_row_anomalies = []
            #
            #         # for checker_class in (CmdRowUfChecker,):
            #         #     checker = checker_class(order_row).check()
            #         #     order_row_anomalies += checker.anomalies
            #
            #         # Interventions liées à cette ligne de commande
            #         analyse_data = {
            #             'unlinked_intvs': matches[3],  # Interventions liées à aucune ligne de la commande
            #             'linked_intvs': matches[0].get(order_row.no_ligne_lc, []),
            #
            #         }
            #         if len(matches[0].get(order_row.no_ligne_lc, [])):
            #             linked_nu_int = matches[0].get(order_row.no_ligne_lc, [])[0][0]
            #             intv = {k: (float(v) if isinstance(v, Decimal) else v)
            #                       for k, v in get_intv(linked_nu_int).items()}
            #             analyse_data['intv'] = intv
            #         else:
            #             analyse_data['intv'] = None
            #
            #             # Stockage de l'analyse globale de la commande dans la première ligne
            #         # order_row.analyse = {
            #         #     'level': max([int(anomaly['code'][0]) for anomaly in order_row_anomalies])
            #                       if order_row_anomalies else 0,
            #         #     'anomalies': order_row_anomalies,
            #         #     'intv': analyse_data['intv'],
            #         #     'unlinked_intvs': analyse_data['unlinked_intvs'],
            #         #     'linked_intvs': analyse_data['linked_intvs'],
            #         # }
            #         # order_row.save()
            #         # print(f"{order_row.commande}-{order_row.no_ligne_lc}: ", end='')
            #         # print([len(t) for t in matcher.get_all_results()])
            #         lc_count += 1
            #
            #     # Stockage de l'analyse globale de la commande dans la première ligne
            #     # order_rows[0].analyse_cmd = {
            #     #     'level': max([int(anomaly['code'][0])
            #               for anomaly in order_anomalies]) if order_anomalies else 0,
            #     #     'anomalies': order_anomalies,
            #     # }
            #     # order_rows[0].save()

            # print(f"Lignes de commande traitées : {lc_count}")

        except DatabaseError as exception:
            self.stdout.write("Asset+ non connecté : « {} ». Commande avortée.".format(str(exception)))
