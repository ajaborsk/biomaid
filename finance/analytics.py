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
import re

from django.apps import apps
from django.db import DatabaseError
from django.db.models import Case, Count, Sum, Value, When
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
from assetplusconnect.models import BEq1996, BFt1996, EnCours
from finance.apps import get_intv_from_order, no_interv_re


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
        order, order_row, interv = self.data
        if interv is not None:
            if interv['n_seri'] not in order_row.libelle:
                self.add(n_seri=interv['n_seri'], nu_int=interv['nu_int'])
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
        order, order_row, interv = self.data
        if interv is not None:
            if interv['nu_imm'] not in order_row.libelle:
                self.add(nu_imm=interv['nu_imm'], nu_int=interv['nu_int'])
        return super().check(verbosity)


class CmdRowUfChecker(RecordAnomalyChecker):
    code = '2L10'
    level = 2
    base_score = 2
    label = _("Commande non saisie dans Asset+")
    message = _("Aucune commande n'a été saisie dans l'intervention Asset+ associée ({nu_int}).")
    description = _("Aucune commande n'a été saisie dans l'intervention Asset+ associée.")
    tips = ''

    def check(self, verbosity=1):
        order, order_row, interv = self.data
        if interv is not None and len(interv['nu_bon_c']) < 2:
            self.add(nu_int=interv['nu_int'])
        return super().check(verbosity)


class CmdRowCmdChecker(RecordAnomalyChecker):
    code = '2L12'
    level = 2
    base_score = 2
    label = _("Non correspondance de l'UF")
    message = _("L'UF spécifiée pour la ligne de commande ({no_uf_uf:04d}) ne correspond pas à l'UF de l'intervention ({n_uf}).")
    description = _("L'UF spécifiée pour la ligne de commande ne correspond pas à l'UF de l'intervention.")
    tips = ''

    def check(self, verbosity=1):
        order, order_row, interv = self.data
        if interv is not None:
            if '{:04d}'.format(order_row.no_uf_uf) != interv['n_uf']:
                self.add(no_uf_uf=order_row.no_uf_uf, n_uf=interv['n_uf'])
        return super().check(verbosity)


class CmdRowNullChecker(RecordAnomalyChecker):
    code = '4L00'
    level = 4
    base_score = 10
    label = _("Ligne avec montant nul")
    message = _("La ligne de commande a un montant d'engagement à 0 €.")
    description = _("La ligne de commande a un montant d'engagement à 0 €.")
    tips = ''

    def check(self, verbosity=1):
        order, order_row = self.data
        if order_row.mt_engage_lc == 0:
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
        order, order_row, interv = self.data
        if interv is not None:
            self.add(
                no_intv=interv['nu_int'],
                strength=100 * interv['match_strength'],
                data={'intv': interv['nu_int'], 'strength': 100 * interv['match_strength']},
            )
        return super().check(verbosity)


class CmdRowNoIntervChecker(RecordAnomalyChecker):
    code = '4L01'
    level = 4
    base_score = 10
    label = _("Ligne avec montant non nul et non rapprochée d'une intervention")
    message = _("La ligne de commande n'a pas pu être rapprochée d'une intervention.")
    description = _(
        "La ligne de commande ne contient pas l'expression 'FRAIS DE...'" " et n'a pas pu être rapprochée d'une intervention."
    )
    tips = ''

    def check(self, verbosity=1):
        order, order_row, interv = self.data
        if interv is None and order_row.mt_engage_lc > 0 and 'FRAIS DE' not in order_row.libelle.upper():
            self.add()
        return super().check(verbosity)


class CmdRowASolderChecker(RecordAnomalyChecker):
    code = '3L01'
    level = 3
    base_score = 5
    label = _("Ligne non soldée alors que l'intervention est archivée.")
    message = _("La ligne de commande n'est pas soldée alors que l'intervention est archivée.")
    description = _("La ligne de commande n'est pas soldée alors que l'intervention associée est archivée.")
    tips = _(
        "Après vérification qu'il s'agit bien de la bonne intervention et que le montant engagé correspond"
        " à ce qui a effectivement été réalisé par le fournisseur, la ligne de commande peut être réceptionnée."
    )

    def check(self, verbosity=1):
        order, order_row, interv = self.data
        if interv is not None and order_row.lg_soldee_lc == 'N' and interv['etat'] == 'Archivée':
            self.add()
        return super().check(verbosity)


class CmdRowBaseChecker(AnomalyChecker):
    """Checker d'une ligne de commande de maintenance à l'attachement
    data est ...(command_as_dict, row_as_record, [interv_as_dict, match_score])"""

    def __init__(self, data):
        super().__init__(data, storage=JsonAnomaliesStorage(data[1], 'analyse'))

    def check(self, verbosity=1):
        if verbosity > 1:
            print(_("  Analyse de la ligne {} :").format(self.data[1].no_ligne_lc))
        self.append(CmdRowNullChecker(data=self.data).check().anomalies)
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
        self.append(CmdRowIntervLinkChecker(data=self.data).check().anomalies)
        self.append(CmdRowUfChecker(data=self.data).check().anomalies)
        self.append(CmdRowNoIntervChecker(data=self.data).check().anomalies)
        self.append(CmdRowASolderChecker(data=self.data).check().anomalies)
        self.append(CmdRowInventChecker(data=self.data).check().anomalies)
        self.append(CmdRowSerialNumberChecker(data=self.data).check().anomalies)
        if verbosity > 1:
            print(_("    Anomalies:"))
            print_anomalies(self.anomalies, indent=6)
        return super().check(verbosity)


class CmdOldChecker(AnomalyChecker):
    code = '2C01'
    level = 2
    message = _("La commande a été passée il y a longtemps ({age} mois) et n'est pas soldée.")

    def check(self, verbosity=1):
        order, rows_anomalies = self.data

        age = (now() - order['date_passation_ec']).days // 30
        if age > 6:
            self.add(age=age, score=age - 6)

        return super().check(verbosity)


class CmdNoIntervChecker(AnomalyChecker):
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
    code = '4C02'
    level = 4
    base_score = 50
    message = 'Commande hors-marché sans dérogation (code HM? dans "objet de la dépense").'
    hm_code_re = re.compile(r'\bHM\d\b')

    def check(self, verbosity=1):
        order, rows_anomalies = self.data

        if not order['no_marche_ma'] and (
            order['objet_depense_ec'] is None or self.hm_code_re.search(order['objet_depense_ec']) is None
        ):
            self.add()

        return super().check(verbosity)


class CmdAnyNullChecker(AnomalyChecker):
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
    code = '2C01'
    level = 2
    base_score = 2
    message = _("Ligne(s) {lignes} de la commande avec au moins une anomalie mineure.")

    def check(self):
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

        return super().check()


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
            row_anomalies[row.no_ligne_lc] = CmdRowBaseChecker(data=(self.data[1], row)).check().anomalies
        self.append(CmdAllNullChecker(data=(self.data[1], row_anomalies)).check(verbosity=verbosity).anomalies)
        self.append(CmdAnyNullChecker(data=(self.data[1], row_anomalies)).check(verbosity=verbosity).anomalies)
        self.append(CmdContractChecker(data=(self.data[1], row_anomalies)).check(verbosity=verbosity).anomalies)
        self.append(CmdOldChecker(data=(self.data[1], row_anomalies)).check(verbosity=verbosity).anomalies)

        if verbosity > 1:
            print(_("  Cmd simple anomalies:"))
            print_anomalies(self.anomalies, indent=4)

        return super().check()


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
        order_rows = self.data[0].objects.filter(commande=self.data[1]['commande']).order_by('no_ligne_lc')

        rows = [
            dict(row, **{'interv': no_interv_re.findall(row['libelle'])})
            for row in order_rows.values(
                'no_ligne_lc',
                'libelle',
                'mt_engage_lc',
                'lg_soldee_lc',
                'commande',
                'no_uf_uf',
            )
        ]

        try:
            intvs = get_intv_from_order(self.data[1], rows)
            matcher = IntvLignesRecordMatcher({row['no_ligne_lc']: row for row in rows}, intvs)
            matches = matcher.get_all_results()

            row_anomalies = {}
            interv_rows = False
            for row in order_rows:
                if str(row.no_compte_cp).startswith('615'):
                    best_match = matches[0].get(row.no_ligne_lc, [None])[0]
                    if best_match is not None:
                        interv = get_intv(best_match[0])
                        interv['match_strength'] = best_match[1]
                    else:
                        interv = None
                    row_anomalies[row.no_ligne_lc] = CmdRowAssetChecker(data=(self.data[1], row, interv)).check().anomalies
                    interv_rows = True

            if interv_rows:
                self.append(CmdNoIntervChecker(data=(self.data[1], row_anomalies)).check().anomalies)
                self.append(CmdSoldeChecker(data=(self.data[1], row_anomalies)).check().anomalies)
                self.append(CmdWarningChecker(data=(self.data[1], row_anomalies)).check().anomalies)
        except DatabaseError:
            self.append([{'code': 'DBERR', 'message': _("Impossible de se connecter à Asset+"), 'level': 1, 'score': 0}])

        if verbosity > 1:
            print(_("  Cmd Asset+ anomalies:"))
            print_anomalies(self.anomalies, indent=4)

        return super().check()


class AllCmdChecker(AnomalySubCheckerMixin, AnomalyChecker):
    """Checker de la totalité des commandes.
    data is the 'ExtCommande' model"""

    def aggregator(self, records):
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

    def add(self, **kwargs):
        key = (kwargs['gest'], kwargs['level'])
        self.storage.add(key)

    def check(self, verbosity=1):
        order_qs = (
            self.data.objects.filter(gest_ec__in=self.kwargs['gestionnaires'], lg_soldee_lc='N')
            .order_by()
            .annotate(
                lg_zero=Case(When(mt_engage_lc__gt=-0.01, mt_engage_lc__lt=0.01, then=Value(1))),
                default=Value(0),
            )
            .annotate(
                lg_soldee=Case(When(lg_soldee_lc='O', lg_zero=0, then=Value(1))),
                default=Value(0),
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
            if cmd_anomalies:
                self.add(
                    level=max(anomaly['level'] for anomaly in cmd_anomalies),
                    gest=order['gest_ec'],
                )
            else:
                self.add(level=0, gest=order['gest_ec'])

        # for gest, gest_anomalies in anomalies.items():
        #     for level, level_anomalies in gest_anomalies.items():
        #         put_data(
        #             source=data_source,
        #             parameters={'gest': gest, 'level': level},
        #             timestamp=timestamp,
        #             data=len(level_anomalies),
        #             link={},
        #             context={},
        #         )

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
        (10, match.Contains('libelle', 'nu_int')),
        (2, match.Contains('libelle', 'nu_imm')),
        (2, match.Contains('libelle', 'n_seri')),
        (0.2, match.Contains('libelle', 'typ_mod')),
        (0.1, match.Contains('libelle', 'marque')),
        (0.1, match.Equal('no_uf_uf', 'n_uf')),
    )


def orders_flaws_processor(*args, **kwargs):

    verbosity = kwargs.get('verbosity') or 0

    print(_("Détection des problèmes liés aux commandes..."))
    ...
    gests = ['IF', 'II', 'IM']
    ext_commande_model = apps.get_model('extable', 'ExtCommande')

    AllCmdChecker(ext_commande_model, gestionnaires=gests).check(verbosity=verbosity)

    print(_("Fait."))
    pass
