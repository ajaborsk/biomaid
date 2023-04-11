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
from copy import copy
from math import fabs
from os import path
import pickle
import re
from typing import Any

from xlsxwriter import Workbook

from assetplusconnect.models import BEq1996, BFt1996, EnCours, Docliste
from django.apps import apps
from django.db import DatabaseError
from django.db.models import Case, Count, Sum, Value, When, F
from django.template.engine import Engine
from django.template import Context
from django.utils.timezone import now
from django.utils.translation import gettext as _

from analytics import match
from analytics.anomaly import (
    AnomalyChecker,
    AnomalySubCheckerMixin,
    DataSourceAnomaliesStorage,
    JsonAnomaliesStorage,
    RecordAnomalyChecker,
    print_anomalies,
)
from analytics.match import RecordMatcher
from analytics.models import DataSource
from common.utils import DataWorksheet
from finance.apps import get_intv_from_order, no_interv_re
from smart_view.smart_expression import find_magh2_order

from dem.models import Demande

serial_re = re.compile(r'(\S*)\s*\(.*\)\s*')
inv_re_list = [
    re.compile(s) for s in (r'\b(\d\d\d\d-\d\d\d\d\d)\b', r'\b(\d\d\d\d-\d\d\d\d\d)-\d\d\b', r'\b(\d\d\d\d.\d\d.\d\d\d)/\d+\b')
]


def order_row_on_work_order(order_row: Any):
    if 'FRAIS ' in order_row.libelle:
        return False
    else:
        return True


def pure_serial(raw_serial: str):
    m = serial_re.match(raw_serial)
    if m is not None:
        return m.group(1)
    return raw_serial


class CmdRowSerialNumberChecker(RecordAnomalyChecker):
    code = '2L11'
    level = 2
    base_score = 2
    label = _("N° de série de l'équipement de l'intervention associée non retrouvé dans la ligne de commande.")
    message = _(
        "N° de série de l'équipement ({n_seri}) de l'intervention associée ({nu_int}) non retrouvé dans la ligne de commande."
    )
    description = _("N° de série de l'équipement de l'intervention associée non retrouvé dans la ligne de commande.")
    tips = ''

    def check(self, verbosity=1):
        order, order_row, interv_list, interv = self.data
        if interv is not None and order_row.qte_cdee_lc == 1 and order_row_on_work_order(order_row):
            if pure_serial(interv['n_seri']) not in order_row.libelle:
                self.add(n_seri=pure_serial(interv['n_seri']), nu_int=interv['nu_int'])
        return super().check(verbosity)


class CmdRowInventChecker(RecordAnomalyChecker):
    code = '2L12'
    level = 2
    base_score = 2
    label = _("N° d'inventaire de l'équipement de l'intervention associée non retrouvé dans la ligne de commande.")
    message = _(
        "N° d'inventaire de l'équipement ({nu_imm}) de l'intervention associée ({nu_int}) non retrouvé dans la ligne de commande."
    )
    description = _("N° d'inventaire de l'équipement de l'intervention associée non retrouvé dans la ligne de commande.")
    tips = ''

    def check(self, verbosity=1):
        order, order_row, interv_list, interv = self.data
        if interv is not None and order_row.qte_cdee_lc == 1 and order_row_on_work_order(order_row):
            if interv['nu_imm'] not in order_row.libelle:
                self.add(nu_imm=interv['nu_imm'], nu_int=interv['nu_int'])
        return super().check(verbosity)


class CmdRowCmdChecker(RecordAnomalyChecker):
    code = '2L10'
    level = 2
    base_score = 2
    label = _("Commande(s) non saisie dans Asset+")
    message = _("Le n° de commande n'a pas été saisi dans toutes les interventions Asset+ associées ({nu_int}).")
    description = _("Le n° de commande n'a pas été saisi dans toutes les interventions Asset+ associées.")
    tips = _(
        "Pour chacune des interventions citées, il faut saisir le numéro de commande dans le "
        "champs 'Numéro de commande' (onglet 'Données économiques')"
    )

    def check(self, verbosity=1):
        order, order_row, interv_list, interv = self.data
        incorrect_work_orders = []
        for work_order in interv_list:
            if len(work_order['nu_bon_c']) < 2 or work_order['nu_bon_c'] != order['commande']:
                incorrect_work_orders.append(work_order['nu_int'])
        if incorrect_work_orders:
            self.add(nu_int=', '.join(incorrect_work_orders))
        return super().check(verbosity)


class CmdRowUfChecker(RecordAnomalyChecker):
    code = '2L12'
    level = 2
    base_score = 2
    label = _("Non correspondance de l'UF")
    message = _(
        "L'UF spécifiée pour la ligne de commande ({no_uf_uf:04d}) ne correspond pas à l'UF"
        " pour certaines interventions ({n_uf})."
    )
    description = _("L'UF spécifiée pour la ligne de commande ne correspond pas aux UF des interventions.")
    tips = ''

    def check(self, verbosity=1):
        order, order_row, interv_list, interv = self.data
        incorrect_work_orders = []
        for work_order in interv_list:
            if '{:04d}'.format(order_row.no_uf_uf) != work_order['n_uf']:
                incorrect_work_orders.append(str(work_order['nu_int']) + '/' + work_order['n_uf'])

        if incorrect_work_orders:
            self.add(no_uf_uf=order_row.no_uf_uf, n_uf=', '.join(incorrect_work_orders))

        return super().check(verbosity)


class CmdRowNullChecker(RecordAnomalyChecker):
    code = '4L00'
    level = 4
    base_score = 10
    label = _("Ligne avec montant nul")
    message = _("La ligne de commande (non soldée) a un montant d'engagement à 0 €.")
    description = _("La ligne de commande (non soldée) a un montant d'engagement à 0 €.")
    tips = ''

    def check(self, verbosity=1):
        order, order_row = self.data
        if order_row.lg_soldee_lc == 'N' and order_row.mt_engage_lc == 0:
            self.add()
        return super().check(verbosity)


class CmdRowIntervLinkChecker(RecordAnomalyChecker):
    code = '1L01'
    level = 1
    base_score = 0
    label = _("Ligne rapprochée d'une intervention")
    message = _("La ligne de commande a pu être rapprochée de l'intervention {no_intv} (qualité: {strength:3.1f}%).")
    description = _("La ligne de commande a pu être rapprochée d'une intervention.")
    tips = ''

    def check(self, verbosity=1):
        order, order_row, interv_list, dummy_interv = self.data
        for interv in interv_list:
            self.add(
                no_intv=interv['nu_int'],
                strength=100 * interv['match_strength'],
                data={'intv': interv['nu_int'], 'strength': 100 * interv['match_strength']},
            )
        return super().check(verbosity)


class CmdRowIntervNoChecker(RecordAnomalyChecker):
    code = '3L04'
    level = 3
    base_score = 10
    label = _("N° d'intervention liée non retrouvé dans le libellé de la commande")
    message = _("N° de l'intervention liée ({n_interv}) non retrouvé dans le libellé de la commande.")
    description = _(
        "Une (unique) intervention a pu être associée à la ligne de commande mais son numéro "
        "n'apparaît pas dans le libellé de la commande."
    )
    tips = ''

    def check(self, verbosity=1):
        order, order_row, interv_list, interv = self.data
        if interv is not None and order_row.qte_cdee_lc == 1 and order_row_on_work_order(order_row):
            if interv['nu_int'] not in order_row.libelle:
                self.add(n_interv=interv['nu_int'])
        return super().check(verbosity)


class CmdRowNoIntervChecker(RecordAnomalyChecker):
    code = '4L01'
    level = 4
    base_score = 10
    label = _("Ligne avec montant non nul et non rapprochée d'une intervention")
    message = _("La ligne de commande n'a pas pu être rapprochée d'une intervention.")
    description = _(
        "La ligne de commande ne contient pas l'expression 'FRAIS ...'" " et n'a pas pu être rapprochée d'une intervention."
    )
    tips = ''

    def check(self, verbosity=1):
        order, order_row, interv_list, interv = self.data
        if interv is None and order_row.mt_engage_lc > 0 and 'FRAIS ' not in order_row.libelle.upper():
            self.add()
        return super().check(verbosity)


class CmdRowASolderChecker(RecordAnomalyChecker):
    """ """

    code = '3L01'
    level = 3
    base_score = 5
    label = _("Ligne à réceptionner.")
    message = _(
        "La quantité reçue ({recues}) de la ligne de commande est inférieur au nombre"
        " d'intervention(s) archivée(s) : {archivees}."
    )
    description = _("La quantité reçue de la ligne de commande est inférieur au nombre" " d'intervention(s) archivée(s).")
    tips = _(
        "Après vérification qu'il s'agit bien de la bonne intervention et que le montant engagé correspond"
        " à ce qui a effectivement été réalisé par le fournisseur, la ligne de commande peut être réceptionnée."
    )

    def check(self, verbosity=1):
        order, order_row, interv_list, interv = self.data
        nb_archivees = 0
        for interv in interv_list:
            if interv['etat'] == 'Archivée':
                nb_archivees += 1
        if nb_archivees > order_row.qte_recue_lc:
            self.add(recues=order_row.qte_recue_lc, archivees=nb_archivees)
        return super().check(verbosity)


class CmdRowBaseChecker(AnomalyChecker):
    """Checker d'une ligne de commande de maintenance à l'attachement
    data est ...(command_as_dict, row_as_record, [interv_as_dict, match_score])"""

    def __init__(self, data):
        super().__init__(data, storage=JsonAnomaliesStorage(data[1], 'analyse'))

    def check(self, verbosity=1):
        if verbosity > 1:
            print(_("  Analyse de la ligne {} :").format(self.data[1].no_ligne_lc))
        self.append(CmdRowNullChecker(data=self.data).check(verbosity=verbosity).anomalies)
        if verbosity > 1:
            print(_("    Anomalies:"))
            print_anomalies(self.anomalies, indent=6)
        return super().check(verbosity)


class CmdRowAssetChecker(AnomalyChecker):
    """Checker d'une ligne de commande de maintenance à l'attachement
    data est ...(command_as_dict, row_as_record, [interv_as_dict, match_score])"""

    def __init__(self, data):
        super().__init__(data, storage=JsonAnomaliesStorage(data[1], 'analyse'))

    def check(self, verbosity=1):
        if verbosity > 1:
            print(_("  Analyse de la ligne {} :").format(self.data[1].no_ligne_lc))
        self.append(CmdRowIntervLinkChecker(data=self.data).check(verbosity=verbosity).anomalies)
        self.append(CmdRowCmdChecker(data=self.data).check(verbosity=verbosity).anomalies)
        self.append(CmdRowUfChecker(data=self.data).check(verbosity=verbosity).anomalies)
        self.append(CmdRowNoIntervChecker(data=self.data).check(verbosity=verbosity).anomalies)
        self.append(CmdRowIntervNoChecker(data=self.data).check(verbosity=verbosity).anomalies)
        self.append(CmdRowASolderChecker(data=self.data).check(verbosity=verbosity).anomalies)
        self.append(CmdRowInventChecker(data=self.data).check(verbosity=verbosity).anomalies)
        self.append(CmdRowSerialNumberChecker(data=self.data).check(verbosity=verbosity).anomalies)
        if verbosity > 1:
            print(_("    Anomalies:"))
            print_anomalies(self.anomalies, indent=6)
        return super().check(verbosity)


class CmdOldChecker(AnomalyChecker):
    """Contrôle si une commande est ancienne"""

    code = '2C01'
    level = 2
    message = _(
        "La commande a été passée il y a longtemps ({age} mois) et n'est pas complètement "
        "soldée ({soldees} soldées sur {lignes} lignes)."
    )

    def check(self, verbosity=1):
        order, rows_anomalies = self.data

        if order['lgs_soldees'] < order['lignes']:
            age = (now() - order['date_passation_ec']).days // 30
            if age > 6:
                self.add(age=age, score=age - 6, soldees=order['lgs_soldees'], lignes=order['lignes'])

        return super().check(verbosity)


class CmdNoIntervChecker(AnomalyChecker):
    """Contrôle si une commande ne peut pas être rapprochée de toutes les interventions nécessaires (au moins une ligne
    a une anomalie 4L01)
    """

    code = '4C03'
    level = 4
    base_score = 80
    message = _("Au moins une ligne de commande ne peut pas être rapprochée d'une intervention.")

    def check(self, verbosity=1):
        order, rows_anomalies = self.data

        if any(['4L01' in list(an['code'] for an in ra) for ra in rows_anomalies.values()]):
            self.add()

        return super().check(verbosity)


class CmdAllNullChecker(AnomalyChecker):
    """Contrôle d'une commande pour vérifier que toutes les lignes ne sont pas à 0 €"""

    code = '4C01'
    level = 4
    base_score = 80
    message = 'Toutes les lignes de la commande sont à 0€.'

    def check(self, verbosity=1):
        order, rows_anomalies = self.data

        if all(['4L00' in list(an['code'] for an in ra) for ra in rows_anomalies.values()]):
            self.add()

        return super().check(verbosity)


class CmdContractChecker(AnomalyChecker):
    """Contrôle qu'une commande est soi en marché soi avec une dérogation"""

    code = '4C02'
    level = 4
    base_score = 50
    message = 'Commande hors-marché sans dérogation (code HM? dans "objet de la dépense").'
    hm_code_re = re.compile(r'\bHM\d\b')

    def check(self, verbosity=1):
        order, rows_anomalies = self.data

        if (
            order['lgs_soldees'] < order['lignes']
            and not order['no_marche_ma']
            and (order['objet_depense_ec'] is None or self.hm_code_re.search(order['objet_depense_ec']) is None)
        ):
            self.add()

        return super().check(verbosity)


class CmdAnyNullChecker(AnomalyChecker):
    """Contrôle si une commande a au moins une ligne avec un montant à 0 € de façon anormale."""

    code = '4C04'
    level = 4
    base_score = 50
    message = 'Au moins une ligne de la commande est à 0€.'

    def check(self, verbosity=1):
        order, rows_anomalies = self.data

        nulls = ['4L00' in list(an['code'] for an in ra) for ra in rows_anomalies.values()]
        if any(nulls) and not all(nulls):
            self.add()

        return super().check(verbosity)


class CmdSoldeChecker(AnomalyChecker):
    """Contrôle si une commande a au moins une ligne qui semble pouvoir être soldée."""

    code = '3C03'
    level = 3
    base_score = 10
    message = 'Au moins une ligne de la commande semble pouvoir être soldée.'

    def check(self, verbosity=1):
        order, rows_anomalies = self.data

        if any(['3L01' in list(an['code'] for an in ra) for ra in rows_anomalies.values()]):
            self.add()

        return super().check(verbosity)


class CmdWarningChecker(AnomalyChecker):
    """Contrôle si une commande a au moins une ligne avec une alerte"""

    code = '3C01'
    level = 3
    base_score = 2
    message = _("Ligne(s) {lignes} de la commande avec au moins une alerte.")

    def check(self, verbosity=1):
        order, rows_anomalies = self.data

        if any([3 in list(an['level'] for an in ra) for ra in rows_anomalies.values()]):
            self.add(
                lignes=', '.join(
                    map(
                        str,
                        filter(
                            lambda lc: 3 in [an['level'] for an in rows_anomalies[lc]],
                            rows_anomalies.keys(),
                        ),
                    )
                )
            )

        return super().check(verbosity=verbosity)


class CmdLowWarningChecker(AnomalyChecker):
    """Contrôle si une commande a au moins une ligne avec une anomalie mineure"""

    code = '2C01'
    level = 2
    base_score = 2
    message = _("Ligne(s) {lignes} de la commande avec au moins une anomalie mineure.")

    def check(self, verbosity=1):
        order, rows_anomalies = self.data

        if any([2 in list(an['level'] for an in ra) for ra in rows_anomalies.values()]):
            self.add(
                lignes=', '.join(
                    map(
                        str,
                        filter(
                            lambda lc: 2 in [an['level'] for an in rows_anomalies[lc]],
                            rows_anomalies.keys(),
                        ),
                    )
                )
            )

        return super().check(verbosity=verbosity)


class CmdCheckerBase(AnomalySubCheckerMixin, AnomalyChecker):
    """Checker d'une commande sans lien avec d'autres bases et notamment Asset+
    data est le couple (model, order) où model est le modèle Django où sont les lignes de commande et order un dict avec les
    données de la commande (notamment entête)"""

    def __init__(self, data):
        # Petit trick ici : Le résultat de l'analyse est stocké dans
        # une des lignes de la commande (celle avec le plus petit numéro de ligne)
        super().__init__(
            data,
            storage=JsonAnomaliesStorage(
                data[0].objects.filter(commande=data[1]['commande']).order_by('no_ligne_lc')[0],
                'analyse_cmd',
            ),
        )

    def check(self, verbosity=1):
        if verbosity > 1:
            print(_("Analyse de la commande {} :").format(self.data[1]['commande']))
        order_rows = self.data[0].objects.filter(commande=self.data[1]['commande']).order_by('no_ligne_lc')
        row_anomalies = {}
        for row in order_rows:
            row_anomalies[row.no_ligne_lc] = CmdRowBaseChecker(data=(self.data[1], row)).check(verbosity=verbosity).anomalies
        self.append(CmdAllNullChecker(data=(self.data[1], row_anomalies)).check(verbosity=verbosity).anomalies)
        self.append(CmdAnyNullChecker(data=(self.data[1], row_anomalies)).check(verbosity=verbosity).anomalies)
        self.append(CmdContractChecker(data=(self.data[1], row_anomalies)).check(verbosity=verbosity).anomalies)
        self.append(CmdOldChecker(data=(self.data[1], row_anomalies)).check(verbosity=verbosity).anomalies)

        if verbosity > 1:
            print(_("  Cmd simple anomalies:"))
            print_anomalies(self.anomalies, indent=4)

        return super().check(verbosity=verbosity)


class CmdCheckerAssetPlus(AnomalySubCheckerMixin, AnomalyChecker):
    """Checker d'une commande de maintenance à l'attachement
    data est le couple (model, order) où model est le modèle Django où sont les lignes de commande et order un dict avec les
    données de la commande (notamment entête)"""

    def __init__(self, data):
        # Petit trick ici : Le résultat de l'analyse est stocké dans une des lignes de la commande (la première trouvée)
        super().__init__(
            data,
            storage=JsonAnomaliesStorage(
                data[0].objects.filter(commande=data[1]['commande']).order_by('no_ligne_lc')[0], 'analyse_cmd', append_mode=True
            ),
        )

    def check(self, verbosity=1):
        if verbosity > 1:
            print(_("Analyse (avec Asset+) de la commande {} :").format(self.data[1]['commande']))
        order_rows = (
            self.data[0]
            .objects.filter(commande=self.data[1]['commande'])
            .annotate(no_fournisseur=F('fournisseur__no_fournisseur_fr'))
            .order_by('no_ligne_lc')
        )

        rows = [
            dict(row, **{'interv': no_interv_re.findall(row['libelle'])})
            for row in order_rows.values(
                'no_ligne_lc',
                'qte_cdee_lc',
                'qte_recue_lc',
                'libelle',
                'mt_engage_lc',
                'lg_soldee_lc',
                'commande',
                'no_uf_uf',
                'no_fournisseur',
            )
        ]

        try:
            intvs = get_intv_from_order(self.data[1], rows)
            matcher = IntvLignesRecordMatcher({row['no_ligne_lc']: row for row in rows}, intvs)
            matches = matcher.get_all_results()

            row_anomalies = {}
            interv_rows = False
            for row in order_rows:
                interv_list = []
                # Try only to match some order line to work orders
                if str(row.no_compte_cp).startswith('615'):
                    for matched_intv in matches[0].get(row.no_ligne_lc, []):
                        interv_list.append(get_intv(matched_intv[0]))
                        interv_list[-1]['match_strength'] = matched_intv[1]
                    best_match = matches[0].get(row.no_ligne_lc, [None])[0]
                    if best_match is not None:
                        interv = get_intv(best_match[0])
                        interv['match_strength'] = best_match[1]
                    else:
                        interv = None
                    row_anomalies[row.no_ligne_lc] = (
                        CmdRowAssetChecker(data=(self.data[1], row, interv_list, interv)).check(verbosity=verbosity).anomalies
                    )
                    interv_rows = True

            if interv_rows:
                self.append(CmdNoIntervChecker(data=(self.data[1], row_anomalies)).check(verbosity=verbosity).anomalies)
                self.append(CmdSoldeChecker(data=(self.data[1], row_anomalies)).check(verbosity=verbosity).anomalies)
                self.append(CmdLowWarningChecker(data=(self.data[1], row_anomalies)).check(verbosity=verbosity).anomalies)
                self.append(CmdWarningChecker(data=(self.data[1], row_anomalies)).check(verbosity=verbosity).anomalies)
        except DatabaseError:
            self.append([{'code': 'DBERR', 'message': _("Impossible de se connecter à Asset+"), 'level': 1, 'score': 0}])

        if verbosity > 1:
            print(_("  Cmd Asset+ anomalies:"))
            print_anomalies(self.anomalies, indent=4)

        return super().check(verbosity=verbosity)


class AllCmdChecker(AnomalySubCheckerMixin, AnomalyChecker):
    """Checker de la totalité des commandes.
    data is the 'ExtCommande' model"""

    def aggregator(self, records) -> list[tuple[dict, int]]:
        aggregates = {(gest, level): 0 for gest in ['IF', 'II', 'IM'] for level in range(5)}
        for record in records:
            if record in aggregates:
                aggregates[record] += 1
        return [({'gest': key[0], 'level': key[1]}, value) for key, value in aggregates.items()]

    def __init__(self, data, **kwargs):
        data_source, ds_created = DataSource.objects.get_or_create(
            code='nb-orders-flaws',
            defaults=dict(
                label=_("Nombre de commandes présentant un problème"),
                description=_(""),
                definition={},
                parameters={
                    'gest': {},
                    'level': {},
                },
            ),
        )
        super().__init__(
            data,
            storage=DataSourceAnomaliesStorage(data_source, aggregator=self.aggregator, timestamp=now()),
            **kwargs,
        )

    def add(self, **kwargs) -> None:
        key = (kwargs['gest'], kwargs['level'])
        self.storage.add(key)

    def check(self, verbosity=1):
        order_qs = (
            # self.data.objects.filter(gest_ec__in=self.kwargs['gestionnaires'], lg_soldee_lc='N')
            self.data.objects.filter(gest_ec__in=self.kwargs['gestionnaires'], exercice_ec=now().year)
            .order_by()
            .annotate(
                lg_zero=Case(When(mt_engage_lc__gt=-0.01, mt_engage_lc__lt=0.01, then=Value(1)), default=Value(0)),
            )
            .annotate(
                lg_soldee=Case(When(lg_soldee_lc='O', then=Value(1)), default=Value(0)),
            )
            .values(
                'commande',
                'gest_ec',
                'no_marche_ma',
                'date_passation_ec',
                'fournisseur__no_fournisseur_fr',
                'fournisseur__intitule_fournisseur_fr',
                'objet_depense_ec',
                'bloc_note',
            )
            .annotate(
                lignes=Count('no_ligne_lc'),
                engage=Sum('mt_engage_lc'),
                liquide=Sum('mt_liquide_lc'),
                lgs_zero=Sum('lg_zero'),
                lgs_soldees=Sum('lg_soldee'),
            )
            .distinct()
            .order_by('date_passation_ec')
        )

        for order in order_qs:
            cmd_anomalies = CmdCheckerBase(data=(self.data, order)).check(verbosity=verbosity).anomalies
            cmd_anomalies += CmdCheckerAssetPlus(data=(self.data, order)).check(verbosity=verbosity).anomalies

            # Only records (for summary) anomalies of still open orders
            if order['lgs_soldees'] < order['lignes']:
                if cmd_anomalies:
                    self.add(
                        level=max(anomaly['level'] for anomaly in cmd_anomalies),
                        gest=order['gest_ec'],
                    )
                else:
                    self.add(level=0, gest=order['gest_ec'])

        return super().check(verbosity=verbosity)


def get_intv(nu_int: str):
    intv = None
    intv_qs = EnCours.objects.using('gmao').filter(nu_int=nu_int).values()
    if len(intv_qs):
        intv = intv_qs[0]
        intv['etat'] = (
            {
                None: _("Inconnu"),
                '1': _("Non visée"),
                '2': _("En cours"),
                '3': _("A récupérer"),
                '4': _("Définitive non archivée"),
            }[intv['int_statut'].strip()]
            + " : "
            + (intv['lib_statut'] if intv['lib_statut'] else '-')
        )
    intv_qs = BFt1996.objects.using('gmao').filter(nu_int=nu_int).values()
    if len(intv_qs):
        intv = intv_qs[0]
        intv['etat'] = _("Archivée")

    if intv:
        eqpt_qs = BEq1996.objects.using('gmao').filter(n_imma=intv['nu_imm']).values('n_seri')
        if len(eqpt_qs) == 1:
            intv['n_seri'] = eqpt_qs[0]['n_seri']
        else:
            intv['n_seri'] = ''
        docs_qs = Docliste.objects.using('gmao').filter(nu_int=nu_int).values('nom_doc').distinct()
        docs = []
        if len(docs_qs):
            docs += [dict(doc) for doc in docs_qs]

        intv['docs'] = '<br/>'.join(
            '<a href="../../common/attachment/gmao/librairie_ASSET/'
            + doc['nom_doc'].split('\\')[-1]
            + '" onclick="window.open(this.href); return false;">'
            + doc['nom_doc'].split('\\')[-1]
            + '</a>'
            for doc in docs
        )
    return intv


class IntvLignesRecordMatcher(RecordMatcher):
    """
    'RecordMatcher' entre les lignes de commandes de magh2 pour la maintenance à l'attachement et les interventions dans Asset+
    Essaye de retrouver dans le libellé de la commande :
    - Le numéro d'intervention (poids 10)
    - Le numéro d'inventaire (poids 2)
    - Le n° de série de l'équipement (poids 2)
    - Le type / modèle de l'équipement (poids 0.2)
    - La marque de l'équipement (poids 0.1)
    """

    criteria = (
        (40, match.Contains('libelle', 'nu_int')),  # On retrouve le numéro d'intervention dans le libellé de la ligne
        (35, match.Equal('commande', 'nu_bon_c')),  # Le numéro de la commande est indiqué dans l'intervention
        (10, match.Equal('no_uf_uf', 'n_uf')),  # L'UF de l'intervention est identique à celle de la ligne
        (10, match.Equal('no_fournisseur', 'code_four')),  # Le fournisseur de l'intervention est identique à celui de la commande
        (2, match.Contains('libelle', 'nu_imm')),  # On retrouve le numéro d'inventaire dans le libellé
        (2, match.Contains('libelle', 'n_seri')),  # On retrouve le numéro de série dans le libellé
        (0.5, match.Contains('libelle', 'typ_mod')),  # On retrouve le type modèle dans le libellé
        (0.5, match.Contains('libelle', 'marque')),  # On retrouver la marque dans le libellé
    )

    cutoff_value = 0.3

    def left_limits(self, left_rec):
        if "FRAIS " in left_rec['libelle']:
            min_matches: int = 0
            max_matches: int = 0
        else:
            min_matches: int = int(left_rec['qte_cdee_lc'])
            max_matches: int = int(left_rec['qte_cdee_lc'])
        return (min_matches, max_matches)

    def prepare(self):
        for left_idx, left_rec in self.left.items():
            left_rec['no_uf_uf'] = '{:04d}'.format(int(left_rec['no_uf_uf']))
        for right_idx, right_rec in self.right.items():
            right_rec['n_seri'] = pure_serial(right_rec['n_seri'])
            right_rec['code_four'] = int(right_rec['code_four'].strip()) if right_rec['code_four'] else None
        super().prepare()


def orders_flaws_processor(*args, **kwargs):

    verbosity = kwargs.get('verbosity') or 0

    print(_("Détection des problèmes liés aux commandes..."))
    ...
    gests = ['IF', 'II', 'IM']
    ext_commande_model = apps.get_model('extable', 'ExtCommande')

    AllCmdChecker(ext_commande_model, gestionnaires=gests).check(verbosity=verbosity)

    print(_("Fait."))
    pass


class PrevAnalyser(RecordAnomalyChecker):
    """
    data is a Previsionnel record
    """

    code = '123'
    level = 0
    message = ""
    template = Engine.get_default().get_template('finance/interface.html')

    def __init__(self, data):
        super().__init__(data, storage=JsonAnomaliesStorage(data, 'analyse'))

    def check(self, verbosity=1):
        # print(f"      DemAnalyse... {self.data[1].code=}")
        dra94_dossier_model = apps.get_model('extable', 'ExtDra94Dossier')
        dra94_ligne_model = apps.get_model('extable', 'ExtDra94Ligne')
        order_row_model = apps.get_model('extable', 'ExtCommande')

        analysis: dict = {}

        manual_orders = find_magh2_order(self.data.suivi_appro)
        if manual_orders:
            no_commandes = set(manual_orders.split())
        else:
            no_commandes = set()

        prev_code_uf = self.data.uf.code

        no_ligne_dra94 = self.data.num_dmd.pk
        code_prog_dra94 = self.data.programme.anteriorite
        if code_prog_dra94:
            dossiers_dra94 = dra94_dossier_model.objects.filter(programme=code_prog_dra94, ligne=no_ligne_dra94)
            analysis['dra'] = []
            for dossier_dra94 in dossiers_dra94:
                analysis['dra'].append(
                    {
                        'code': 'DRA' + str(dossier_dra94.numero)[:4] + '-' + str(dossier_dra94.numero)[4:],
                        'date': str(dossier_dra94.date_dossier),
                        'montant': float(dossier_dra94.montant),
                        'code_fournisseur': int(dossier_dra94.code_fournisseur),
                        'fournisseur': str(dossier_dra94.fournisseur),
                        'no_commande': str(dossier_dra94.no_commande),
                        'date_commande': str(dossier_dra94.date_commande),
                    }
                )
                if dossier_dra94.no_commande:
                    no_commandes.add(str(dossier_dra94.no_commande))
                lignes_dra94 = dra94_ligne_model.objects.filter(dossier=dossier_dra94)
                analysis['dra'][-1]['lignes'] = []
                for ligne in lignes_dra94:
                    analysis['dra'][-1]['lignes'].append(
                        {
                            'code_uf': str(ligne.code_uf),
                            'qte': int(ligne.quantite),
                            'designation': str(ligne.designation),
                            'montant': float(ligne.montant),
                        }
                    )
        commandes_analysis = []
        commandes_on_uf_analysis = []
        prev_mt_engage = 0
        prev_mt_engage_on_uf = 0
        prev_mt_liquide = 0
        prev_mt_liquide_on_uf = 0
        for no_commande in no_commandes:
            rows_on_uf = 0
            order_rows = order_row_model.objects.filter(commande=no_commande)
            mt_engage = 0
            mt_liquide = 0
            for row in order_rows:
                # print(row)
                row_uf = '{:04d}'.format(row.no_uf_uf)
                mt_engage += row.mt_engage_lc or 0
                mt_liquide += row.mt_liquide_lc or 0
                if row_uf == prev_code_uf:
                    rows_on_uf += 1
                    prev_mt_engage_on_uf += row.mt_engage_lc or 0
                    prev_mt_liquide_on_uf += row.mt_liquide_lc or 0
            if rows_on_uf:
                commandes_on_uf_analysis.append(
                    {
                        'no_commande': no_commande,
                        'rows_found': rows_on_uf,
                        'mt_engage': prev_mt_engage_on_uf,
                        'mt_liquide': prev_mt_liquide_on_uf,
                    }
                )
            commandes_analysis.append(
                {
                    'no_commande': no_commande,
                    'rows_found': len(order_rows),
                    'mt_engage': mt_engage,
                    'mt_liquide': mt_liquide,
                }
            )
            prev_mt_engage += mt_engage
            prev_mt_liquide += mt_liquide
        analysis['commandes'] = commandes_analysis
        analysis['commandes_sur_uf'] = commandes_on_uf_analysis
        analysis['mt_engage'] = prev_mt_engage
        analysis['mt_liquide'] = prev_mt_liquide

        try:
            eqpts = []
            for no_commande in no_commandes:
                eqpts += list(BEq1996.objects.using('gmao').filter(n_order__contains=no_commande))
            # print(eqpts)
            analysis_eqpts = []
            analysis_eqpts_uf = []
            eqpts_montant = 0
            eqpts_montant_uf = 0
            for eqpt in eqpts:
                analysis_eqpts.append(
                    {
                        'code': eqpt.n_imma,
                        'code_uf': eqpt.n_uf,
                        'mise_en_service': eqpt.mes1,
                        'prix': float(eqpt.prix),
                    }
                )
                eqpts_montant += float(eqpt.prix)
                if eqpt.n_uf == prev_code_uf:
                    analysis_eqpts_uf.append(
                        {
                            'code': eqpt.n_imma,
                            'mise_en_service': eqpt.mes1,
                            'prix': float(eqpt.prix),
                        }
                    )
                    eqpts_montant_uf += float(eqpt.prix)
            analysis['equipements'] = analysis_eqpts
            analysis['equipements_uf'] = analysis_eqpts_uf
            analysis['equipements_amount'] = eqpts_montant
            analysis['equipements_uf_amount'] = eqpts_montant_uf

            # A small hack here, since we don't have (yet) a API to sava data in multiple fields
            self.data.interface = 'Montant équipements : {equipements_amount:8.2f} €\nMontant engagé : {mt_engage:8.2f} €'.format(
                **analysis
            )
            self.data.interface = self.template.render(Context(analysis))
            self.data.nombre_commandes = len(analysis['commandes'])
            self.data.nombre_lignes_commandes = sum(cmd['rows_found'] for cmd in analysis['commandes'])
            self.data.nombre_equipements = len(analysis['equipements'])
            self.data.valeur_inventaire = analysis['equipements_amount']
            self.data.montant_engage = analysis['mt_engage']
            self.data.montant_liquide = analysis['mt_liquide']

            self.data.save(
                update_fields=[
                    'interface',
                    'nombre_commandes',
                    'nombre_lignes_commandes',
                    'valeur_inventaire',
                    'montant_engage',
                    'montant_liquide',
                    'nombre_equipements',
                    'date_modification',
                ]
            )
        except DatabaseError:
            pass

        # print(analysis)
        self.add(data=analysis)


class DemAnalyser(RecordAnomalyChecker):
    code = '123'
    level = 1
    message = 'test'

    def __init__(self, data):
        super().__init__(data, storage=JsonAnomaliesStorage(data[1], 'analyse'))

    def check(self, verbosity=1):
        # print(f"      DemAnalyse... {self.data[1].code=}")
        for prev in self.data[1].previsionnel_set.all():
            PrevAnalyser(prev).check(verbosity=verbosity)
        self.add(data={'argl': 'ok'})


class DemAllAnalyser(AnomalyChecker):
    def check(self, verbosity=1):
        # print(f"    DemAllAnalyser... {self.data=}")
        qs = self.data.objects.filter()
        for demande in qs:
            DemAnalyser(data=(self.data, demande)).check(verbosity=verbosity)
        return super().check(verbosity=verbosity)


def dem_financial_assess(*args, **kwargs):
    verbosity = kwargs.get('verbosity') or 0
    DemAllAnalyser(Demande).check(verbosity=verbosity)


class ImmoMatchOkChecker(AnomalyChecker):
    """Add links informations if the asset (immo) can be found in (maintenance) inventory"""

    code = '100'
    level = 1
    message = 'Correspondance trouvée : {id} - {name}, UF {uf}, Montant {amount}, MeS {mes}'

    def check(self, verbosity=1):
        idx, idx2, orders_idx, immo = self.data
        if immo.fiche in idx2:
            ids = []
            for id in (
                idx2[immo.fiche]['main']
                + idx2[immo.fiche]['internal']
                + idx2[immo.fiche]['manual']
                + idx2[immo.fiche]['comment']
                + idx2[immo.fiche]['sameorder']
            ):
                if id not in ids:
                    self.add(
                        id=id,
                        name=idx[id]['nom'],
                        uf=idx[id]['n_uf'],
                        amount=str(idx[id]['prix']) + ' €',
                        mes=str(idx[id]['mes1']),
                        data={
                            'eqpt': {
                                'prix': float(idx[id]['prix']) if idx[id]['prix'] != '' else None,
                            },
                            'idx2': idx2[immo.fiche],
                        },
                    )
                    idx[id]['link'] = immo.fiche
                ids.append(id)
            if immo.commande in orders_idx:
                for id in orders_idx[immo.commande]:
                    if id not in ids:
                        self.add(
                            id=id,
                            name=idx[id]['nom'],
                            uf=idx[id]['n_uf'],
                            amount=str(idx[id]['prix']) + ' €',
                            mes=str(idx[id]['mes1']),
                            data={
                                'eqpt': {
                                    'prix': float(idx[id]['prix']) if idx[id]['prix'] != '' else None,
                                },
                                'idx2': idx2[immo.fiche],
                            },
                        )
                        idx[id]['link'] = immo.fiche
                    ids.append(id)

        return super().check(verbosity)


class ImmoMatchNoOkChecker(AnomalyChecker):
    """Add an anomaly if the Asset (immo) cannot be found in the (maintenance) inventory"""

    code = '300'
    level = 3
    message = 'Correspondance non trouvée'

    def check(self, verbosity=1):
        if self.data[3].fiche not in self.data[1]:
            self.add()
        return super().check(verbosity)


class ImmoAmountChecker(AnomalyChecker):
    """Check amount more than 1% diff raise an anomaly"""

    code = '201'
    level = 2
    message = 'Montant total trop différent {amount_immo} != {amount_total}'

    def check(self, verbosity=1):
        idx, idx2, orders_idx, immo, matches = self.data
        amount_immo = float(immo.actif_uf_df2)
        amount_total = 0
        for anomaly in matches:
            try:
                amount_total += float(anomaly['data']['eqpt']['prix'])  # / 0.9605  # This coef is only since ####
            except (ValueError, TypeError):
                pass
        if len(matches) and fabs(amount_immo - amount_total) > amount_immo * 0.01:
            self.add(amount_total=amount_total, amount_immo=amount_immo)
        return super().check(verbosity)


class ImmoUfChecker(AnomalyChecker):
    """Check for UF anomaly"""

    code = '202'
    level = 2
    message = 'UF différente {amount_immo} != {amount_total}'

    def check(self, verbosity=1):
        idx, idx2, orders_idx, immo, matches = self.data
        return super().check(verbosity)


class ImmoCommissioningChecker(AnomalyChecker):
    """Check for Commissioning anomaly
    fr: (Date de mise en service)"""

    code = '203'
    level = 2
    message = 'Date de mise en service trop différente {amount_immo} != {amount_total}'

    def check(self, verbosity=1):
        idx, idx2, orders_idx, immo, matches = self.data
        return super().check(verbosity)


class ImmoReformChecker(AnomalyChecker):
    """Check for Commissioning anomaly
    fr: (Date de mise en service)"""

    code = '301'
    level = 3
    message = 'Equipement réformé dans l\'inventaire technique {amount_immo} != {amount_total}'

    def check(self, verbosity=1):
        idx, idx2, orders_idx, immo, matches = self.data
        return super().check(verbosity)


class ImmoAnalyser(RecordAnomalyChecker):
    """data = (inv_idx_as_dict, inv_idx2_as_dict, immo_as_row)"""

    code = '999'
    level = 1
    message = 'test'

    def __init__(self, data):
        super().__init__(data, storage=JsonAnomaliesStorage(data[3], 'analyse'))

    def check(self, verbosity=1):
        if verbosity >= 3:
            print(_("  Analyse de la fiche {} :").format(self.data[1].code))
        matches = ImmoMatchOkChecker(data=self.data).check(verbosity=verbosity).anomalies
        self.append(matches)
        self.append(ImmoMatchNoOkChecker(data=self.data).check(verbosity=verbosity).anomalies)
        # self.append(
        #     ImmoAmountChecker(data=(self.data[0], self.data[1], self.data[2], self.data[3], matches))
        #     .check(verbosity=verbosity)
        #     .anomalies
        # )


class ImmoAllAnalyser(AnomalyChecker):
    def check(self, verbosity=1):
        print(f"    ImmoAllAnalyser... {self.data=}")

        # Cache filenames
        inv_cache_fn = 'B_EQ1996.cache.pickle'
        idx_cache_fn = 'B_EQ1996_idx.cache.pickle'
        idx2_cache_fn = 'B_EQ1996_idx2.cache.pickle'
        orders_idx_cache_fn = 'B_EQ1996_orders_idx.cache.pickle'

        # Step 2 : Get inventory (main) index from cache or compute it
        print("2 - Getting computed inventory index...")
        if path.exists(idx_cache_fn) and path.exists(orders_idx_cache_fn):
            with open(idx_cache_fn, "rb") as f:
                inv_idx = pickle.load(f)
            with open(orders_idx_cache_fn, "rb") as f:
                orders_idx = pickle.load(f)
            print("  2.0 - Got computed inventory index from cache")
        else:
            # Step 2.1 : Get inventory from cache or from Asset+ Database
            print("  2.1 - Getting inventory...")
            if path.exists(inv_cache_fn):
                with open(inv_cache_fn, "rb") as f:
                    inv = pickle.load(f)
                print("    2.1.0 - Got inventory from cache")
            else:
                qs = BEq1996.objects.using('gmao').all().values()
                qs._fetch_all()
                inv = list(qs)
                with open(inv_cache_fn, "wb") as f:
                    pickle.dump(inv, f)
                print("    2.1.1 - Got inventory from database then stored it to cache")

            print(f"{len(inv)=}")
            inv_idx = {}
            orders_idx = {}
            for eqpt in inv:
                inv_idx[eqpt['n_imma']] = eqpt
                n_order = eqpt['n_order'].upper().strip().replace(' ', '')
                if len(n_order) == 8:
                    if n_order not in orders_idx:
                        orders_idx[n_order] = []
                    orders_idx[n_order].append(eqpt['n_imma'])
            with open(idx_cache_fn, "wb") as f:
                pickle.dump(inv_idx, f)
            with open(orders_idx_cache_fn, "wb") as f:
                pickle.dump(orders_idx, f)
            print("  2.2 - Computed inventory index and stored to cache")
        print(f"{len(inv_idx)=}")

        # Step 3 : Get inventory (rich) index from cache or compute it
        cc = 0
        c_err = 0
        if path.exists(idx2_cache_fn):
            with open(idx2_cache_fn, "rb") as f:
                inv_idx2 = pickle.load(f)
            print("3 - Got rich inventory index")
        else:
            inv_idx2 = {}
            for n_imma, eqpt in inv_idx.items():
                # 3.1 - Calculer le code immo à partir du numéro d'intventaire (si possible)
                if len(n_imma) >= 10 and n_imma[0:4].isdigit() and n_imma[4] == '-' and n_imma[5:10].isdigit():
                    n_immo = n_imma[0:10]
                    if n_immo not in inv_idx2:
                        inv_idx2[n_immo] = copy({'main': [], 'internal': [], 'manual': [], 'comment': [], 'sameorder': []})
                    inv_idx2[n_immo]['main'].append(n_imma)
                    cc += 1
                elif (
                    len(n_imma) >= 12
                    and n_imma[0:4].isdigit()
                    and n_imma[4] == '.'
                    and n_imma[5:7].isdigit()
                    and n_imma[7] == '.'
                    and n_imma[8:11].isdigit()
                ):
                    n_immo = n_imma[0:4] + '-' + n_imma[5:7] + n_imma[8:11]
                    if n_immo not in inv_idx2:
                        inv_idx2[n_immo] = copy({'main': [], 'internal': [], 'manual': [], 'comment': [], 'sameorder': []})
                    inv_idx2[n_immo]['main'].append(n_imma)
                    cc += 1
                else:
                    # print(f"3.1 - Unable to compute n_immo for {n_imma}")
                    c_err += 1
                    eqpt['analyse'] = {'anomalies': [{'label': 'Numéro d\'inventaire non conforme !'}]}

                # 3.2 - Numéro interne
                if (
                    len(eqpt['number_in_site']) >= 10
                    and eqpt['number_in_site'][0:4].isdigit()
                    and eqpt['number_in_site'][4] == '-'
                    and eqpt['number_in_site'][5:10].isdigit()
                ):
                    n_immo = eqpt['number_in_site'][0:10]
                    if n_immo not in inv_idx2:
                        inv_idx2[n_immo] = copy({'main': [], 'internal': [], 'manual': [], 'comment': [], 'sameorder': []})
                    inv_idx2[n_immo]['internal'].append(n_imma)
                elif (
                    len(eqpt['number_in_site']) >= 12
                    and eqpt['number_in_site'][0:4].isdigit()
                    and eqpt['number_in_site'][4] == '.'
                    and eqpt['number_in_site'][5:7].isdigit()
                    and eqpt['number_in_site'][7] == '.'
                    and eqpt['number_in_site'][8:11].isdigit()
                ):
                    n_immo = eqpt['number_in_site'][0:4] + '-' + eqpt['number_in_site'][5:7] + eqpt['number_in_site'][8:11]
                    if n_immo not in inv_idx2:
                        inv_idx2[n_immo] = copy({'main': [], 'internal': [], 'manual': [], 'comment': [], 'sameorder': []})
                    inv_idx2[n_immo]['internal'].append(n_imma)

                # 3.3 - Numéro "code immobilisation" dans les champs libres
                # TODO...
                if (
                    len(eqpt['filler_eco_3']) >= 10
                    and eqpt['filler_eco_3'][0:4].isdigit()
                    and eqpt['filler_eco_3'][4] == '-'
                    and eqpt['filler_eco_3'][5:10].isdigit()
                ):
                    n_immo = eqpt['filler_eco_3'][0:10]
                    if n_immo not in inv_idx2:
                        inv_idx2[n_immo] = copy({'main': [], 'internal': [], 'manual': [], 'comment': [], 'sameorder': []})
                    inv_idx2[n_immo]['manual'].append(n_imma)
                elif (
                    len(eqpt['filler_eco_3']) >= 12
                    and eqpt['filler_eco_3'][0:4].isdigit()
                    and eqpt['filler_eco_3'][4] == '.'
                    and eqpt['filler_eco_3'][5:7].isdigit()
                    and eqpt['filler_eco_3'][7] == '.'
                    and eqpt['filler_eco_3'][8:11].isdigit()
                ):
                    n_immo = eqpt['filler_eco_3'][0:4] + '-' + eqpt['filler_eco_3'][5:7] + eqpt['filler_eco_3'][8:11]
                    if n_immo not in inv_idx2:
                        inv_idx2[n_immo] = copy({'main': [], 'internal': [], 'manual': [], 'comment': [], 'sameorder': []})
                    inv_idx2[n_immo]['manual'].append(n_imma)

                # 3.2 - Numéro qui ressemble dans les commentaires
                for regexp in inv_re_list:
                    if found := regexp.findall(eqpt['nom2']):
                        # print(f"Found inv in comment: {found} {eqpt['nom2']}")
                        for n_immo in found:
                            if n_immo not in inv_idx2:
                                inv_idx2[n_immo] = copy({'main': [], 'internal': [], 'manual': [], 'comment': [], 'sameorder': []})
                            inv_idx2[n_immo]['comment'].append(n_imma)

                # 3.2 - Premier numéro de la fiche d'inventaire du premier équipement de la commande
                # TODO...

            with open(idx2_cache_fn, "wb") as f:
                pickle.dump(inv_idx2, f)
            print("3 - Computed rich inventory index and stored to cache")
        print(f"nb_immo={len(inv_idx2)}, nb eqpts={cc}, nb err={c_err}")

        try:
            immo_model = apps.get_model('extable.ExtImmobilisation')
        except LookupError:
            immo_model = None
        if immo_model:
            immo_found = 0
            immo_not_found = 0
            actif_found = 0
            actif_not_found = 0
            for immo in immo_model.objects.all():
                ImmoAnalyser((inv_idx, inv_idx2, orders_idx, immo)).check(verbosity=verbosity)
                if immo.fiche in inv_idx2:
                    immo_found += 1
                    actif_found += immo.actif_uf_df2
                else:
                    immo_not_found += 1
                    actif_not_found += immo.actif_uf_df2
                    if verbosity >= 3:
                        print(immo.fiche, immo.fiche in inv_idx2, immo.actif_uf_df2)
            print(f"{immo_found=}, {actif_found=}, {immo_not_found=}, {actif_not_found=}")
        else:
            print("Error, cannot find Assets table")

        wb = Workbook(now().strftime('%Y-%m-%d') + ' - asset_vs_madrid.xlsx', {'remove_timezone': True})
        wd = DataWorksheet(
            wb,
            _("Feuille"),
            {
                'code': {},
                'nom': {},
                'prix': {},
                'commande': {'title': 'N° Commande'},
                'classe': {'title': 'Classe'},
                'compte': {'title': 'Compte'},
                'mes': {'title': 'Mise en service'},
                'reforme': {'title': 'Réforme'},
                'link': {'title': 'Lien Madrid'},
            },
            None,
        )
        wd.prepare()
        for n_imma in sorted(inv_idx.keys()):
            eqpt = inv_idx[n_imma]
            # print(f"{eqpt=}")
            if (
                len(eqpt['date_refor']) < 5
                and eqpt['prix'] != ''
                and (eqpt['filler_eco_2'] == 'C2' or eqpt['fk_budget_nu_compte'].startswith('H2') or float(eqpt['prix']) >= 1000)
            ):
                record = {
                    'code': n_imma,
                    'nom': eqpt['nom'],
                    'prix': eqpt['prix'],
                    'commande': eqpt['n_order'],
                    'classe': eqpt['filler_eco_2'],
                    'compte': eqpt['fk_budget_nu_compte'],
                    'mes': eqpt['mes1'],
                    'reforme': eqpt['date_refor'],
                    'link': eqpt.get('link', 'ø'),
                }
                wd.put_row(record)
        wd.finalize()
        wb.close()

        return super().check(verbosity=verbosity)


def immo_financial_assess(*args, **kwargs):
    verbosity = kwargs.get('verbosity') or 0
    ImmoAllAnalyser().check(verbosity=verbosity)
