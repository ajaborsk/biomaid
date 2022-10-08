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
from __future__ import annotations

import re
from decimal import Decimal

import pandas
from django.db.models import F, Sum, QuerySet
from pandas import DataFrame, concat
from xlsxwriter import Workbook

from django.utils.translation import gettext as _
from django.core.management.base import BaseCommand, CommandError

from common import config
from common.models import Programme
from dem.models import Demande
from dra94.models import Dra94Dossier
from drachar.models import Previsionnel
from common.utils import DataWorksheet

# Expression régulière qui 'match' avec un numéro de commande MAGH2
cmd_re = re.compile(r'\b([A-Za-z0-9][A-Za-z0-9]\d\d\d\d\d\d)\b')


def number_cv(data):
    if data:
        return Decimal(data.replace(',', '.'))
    else:
        return None


def write_df_to_worksheet(wb: Workbook, ws_name: str, data_frame: DataFrame, formats: None | dict = None):
    i_formats = {colname: {} for colname in data_frame.columns}
    i_formats.update(formats or {})
    dw = DataWorksheet(wb, ws_name, i_formats)
    dw.prepare()
    dw.put_data_frame(data_frame)
    dw.finalize()
    return dw.ws


def write_qs_to_worksheet(
    wb: Workbook,
    ws_name: str,
    queryset: QuerySet,
    columns: tuple = (),
    formats: dict = {},
):
    df = DataFrame(list(queryset.values(*columns)), columns=columns)
    return write_df_to_worksheet(wb, ws_name, df, formats)


class Command(BaseCommand):
    help = _("Rapport d'utilisation d'un programme")

    def add_arguments(self, parser):
        parser.add_argument('code_programme', type=str)
        parser.add_argument('filename', type=str, nargs='?', default=None)

    def get_demandes(self, programme, validees=None):
        if validees is None:
            demandes = Demande.objects.filter(programme=programme)
        elif validees:
            demandes = Demande.objects.filter(programme=programme, gel=True, arbitrage_commission__valeur=True)
        else:
            demandes = Demande.objects.filter(programme=programme, gel=True, arbitrage_commission__valeur=False)
        return demandes

    def handle(self, *args, **options):
        ret_str = ""
        synthese_data = {}

        try:
            programme = Programme.objects.get(code=options['code_programme'])
        except Programme.DoesNotExist:
            raise CommandError(
                _("Le programme {} n'existe pas. Liste des programmes valides :\n{}").format(
                    options['code_programme'],
                    ', '.join(Programme.objects.all().values_list('code', flat=True)),
                )
            )

        filename = options['filename'] or "rapport-" + options['code_programme'] + '.xlsx'
        ret_str += _("Rapport pour le programme {} dans le fichier {}\n").format(options['code_programme'], filename)
        wb = Workbook(filename, {'nan_inf_to_errors': True})

        synthese_ws = wb.add_worksheet('Synthèse')

        synthese_data['dem_total'] = {
            'label': _("Demandes au total"),
            'value': self.get_demandes(programme).count(),
        }
        synthese_data['dem_ok'] = {
            'label': _("Demandes acceptées"),
            'value': self.get_demandes(programme, True).count(),
        }
        synthese_data['dem_ko'] = {
            'label': _("Demandes refusées"),
            'value': self.get_demandes(programme, False).count(),
        }
        synthese_data['dem_ec'] = {
            'label': _("Demandes en cours"),
            'value': synthese_data["dem_total"]['value'] - synthese_data['dem_ok']['value'] - synthese_data['dem_ko']['value'],
        }
        demandes = self.get_demandes(programme, True)
        synthese_data['dem_ok_amount'] = {
            'label': _("Montant Demandes acceptées"),
            'value': demandes.aggregate(Sum('enveloppe_allouee'))['enveloppe_allouee__sum'],
        }
        write_qs_to_worksheet(wb, 'Demandes', demandes, ('code', 'libelle'))

        previsionnel_qs = Previsionnel.objects.filter(programme=programme).annotate(
            libelle=F('num_dmd__libelle'), code_programme=F('programme__code')
        )
        write_qs_to_worksheet(
            wb,
            'Demandes acceptées',
            previsionnel_qs,
            (
                'code_programme',
                'num_dmd_id',
                'libelle',
                'budget',
                'suivi_appro',
                'suivi_mes',
            ),
            {
                'code_programme': {
                    'title': _("Programme"),
                    'width': 15,
                },
                'num_dmd_id': {
                    'title': _("Ligne"),
                    'width': 8,
                },
                'libelle': {
                    'title': _("Libellé"),
                    'width': 50,
                },
                'budget': {
                    'title': _("Enveloppe"),
                    'cell': {'num_format': '_-* # ##0,00 €_-;-* # ##0,00 €_-;_-* "-"?? €_-;_-@_-'},
                },
                'suivi_appro': {
                    'title': _("DRA / Commande"),
                    'width': 20,
                },
                'suivi_mes': {
                    'title': _("Mise en service"),
                    'width': 20,
                },
            },
        )
        cmd_prev = {}
        for instance in previsionnel_qs:
            commandes = map(
                lambda s: s.upper(),
                cmd_re.findall(instance.suivi_appro) if instance.suivi_appro else [],
            )
            for commande in commandes:
                cmd_prev[commande] = cmd_prev.get(commande, []) + [instance]
        # pprint(cmd_prev)

        dra_qs = Dra94Dossier.objects.filter(
            programme=programme.anteriorite,
            ligne__in=previsionnel_qs.values('num_dmd_id'),
        )
        synthese_data['dra_nb'] = {
            'label': _("Nombre de DRA du programme"),
            'value': dra_qs.count(),
        }

        # Dictionnaire qui associe une instance de DRA à chaque commande (qui existe)
        cmd_dra = {instance.no_commande: instance for instance in dra_qs}

        # On écrit la table des DRA dans le classeur
        write_qs_to_worksheet(wb, 'DRA', dra_qs, ('programme', 'ligne', 'no_commande'))

        # Ensemble de toutes les commandes concernées par le programme
        all_commandes = set(cmd_dra.keys()) | set(cmd_prev.keys())

        # ws = wb.add_worksheet('Lignes DRA')

        # ws = wb.add_worksheet('Commandes')
        # Lit toutes les commandes dans un DataFrame
        commande_df = pandas.read_csv(
            config.settings.MAGH2_CFG['data_path'] + 'commandes_c2.csv',
            low_memory=False,
            converters={'Mt Engagé (lc)': number_cv, 'Mt liquidé (lc)': number_cv},
            parse_dates=['Date Passation (ec)'],
            dayfirst=True,
        )
        # Crée une colonne avec le numéro de colonne complet
        commande_df['no_commande'] = commande_df.apply(
            lambda row: '{:2s}{:06d}'.format(row['Gest. (ec)'], int(row['No Cde (ec)'])),
            axis=1,
        )
        # Ne conserve que les commandes liées à ce programme (en passant par les numéros de commande
        commande_df = commande_df[commande_df.apply(lambda row: row['no_commande'] in all_commandes, axis=1)]
        # print("Lignes de ce programme =", len(commande_df))
        write_df_to_worksheet(
            wb,
            'Commandes',
            commande_df,
            {
                'Gest. (ec)': {
                    'title': _("Gest"),
                },
                'Date Passation (ec)': {
                    'title': _("Passation"),
                    'width': 13,
                    'cell': {'num_format': 'dd/mm/yy'},
                },
                'Libellé UF (uf)': {
                    'title': _("Nom UF"),
                    'width': 30,
                },
                'Mt Engagé (lc)': {
                    'title': _("Engagé"),
                    'cell': {'num_format': '# ##0,00 [$€-40C];-# ##0,00 [$€-40C]'},
                },
            },
        )

        immobilisation_df = pandas.read_csv(
            config.settings.MAGH2_CFG['data_path'] + 'amortissements.csv',
            low_memory=False,
            converters={'Actif UF (df2)': number_cv},
            parse_dates=['Date de mise en service (fi)', 'DF Amort (fi2)'],
            dayfirst=True,
        )
        # print("Toutes les immos =", len(immobilisation_df))
        immobilisation_df = immobilisation_df[
            immobilisation_df.apply(
                lambda row: isinstance(row['Gest Cde (df)'], str)
                and '{:2s}{:06d}'.format(row['Gest Cde (df)'], int(row['No Cde (df)'])) in all_commandes,
                axis=1,
            )
        ]
        if len(immobilisation_df):
            immobilisation_df['no_commande'] = immobilisation_df.apply(
                lambda row: '{:2s}{:06d}'.format(row['Gest Cde (df)'], int(row['No Cde (df)'])),
                axis=1,
            )

        DataWorksheet(
            wb,
            "Fiches Madrid",
            {
                "Exercice d'acquisition (fi)": {},
                'No Fiche (fi)': {},
                'Gest Cde (df)': {},
                'No Cde (df)': {},
                'no_commande': {},
                'Ligne Commande (df)': {},
                'Compte Ordonnateur (cp)': {},
                'Libellé Compte (cp)': {'width': 50},
                'Libellé du bien (fi)': {'width': 60},
                'Mode Gest (fi1)': {'title': _("Mode")},
                'Date de mise en service (fi)': {
                    'title': _("Date MES"),
                    'cell': {'num_format': 'MM/DD/YY'},
                },
                'Durée (fi2)': {'title': _("Durée Amort")},
                'DF Amort (fi2)': {
                    'title': _("Fin Amort"),
                    'cell': {'num_format': 'MM/DD/YY'},
                },
                'No UF (df)': {'title': _("UF")},
                'Libellé UF (df)': {'title': _("Libellé UF"), 'width': 50},
                'Qté UF (df1)': {'title': _("Qté UF")},
                'Répart. UF (df1)': {},
                'Répartition (fi1)': {},
                'Code Famille (fe)': {},
                'Libellé Famille (fe)': {'width': 50},
                'No Interne (fi)': {},
                'Actif UF (df2)': {'cell': {'num_format': '# ##0,00 [$€-40C];-# ##0,00 [$€-40C]'}},
            },
        ).prepare().put_data_frame(immobilisation_df).finalize()

        row_idx = 2
        for label, data in synthese_data.items():
            synthese_ws.write(row_idx, 1, data['label'] + " :")
            synthese_ws.write(row_idx, 2, data['value'])
            row_idx += 1

        dws = DataWorksheet(
            wb,
            'Complet',
            {
                # Prévisionnel DRA
                'code_programme': {
                    'title': _("Programme"),
                    'width': 15,
                },
                'num_dmd_id': {
                    'title': _("Ligne"),
                    'width': 8,
                },
                'libelle': {
                    'title': _("Libellé"),
                    'width': 50,
                },
                'budget': {
                    'title': _("Enveloppe"),
                    'cell': {'num_format': '_-* # ##0,00 €_-;-* # ##0,00 €_-;_-* "-"?? €_-;_-@_-'},
                },
                'suivi_appro': {
                    'title': _("DRA / Commande"),
                    'width': 20,
                },
                'suivi_mes': {
                    'title': _("Mise en service"),
                    'width': 20,
                },
                # Commandes
                'no_commande': {
                    'title': _("Commande"),
                },
                'Gest. (ec)': {
                    'title': _("Gest"),
                },
                'Date Passation (ec)': {
                    'title': _("Passation"),
                    'width': 13,
                    'cell': {'num_format': 'dd/mm/yy'},
                },
                'No Ligne (lc)': {
                    'title': _("Ligne Cmd"),
                },
                'Libellé UF (uf)': {
                    'title': _("Nom UF"),
                    'width': 30,
                },
                'Mt Engagé (lc)': {
                    'title': _("Engagé"),
                    'cell': {'num_format': '# ##0,00 [$€-40C];-# ##0,00 [$€-40C]'},
                },
                # Fiches immobilisation
                "Exercice d'acquisition (fi)": {},
                'No Fiche (fi)': {},
                'Gest Cde (df)': {},
                'No Cde (df)': {},
                'Ligne Commande (df)': {},
                'Compte Ordonnateur (cp)': {},
                'Libellé Compte (cp)': {'width': 50},
                'Libellé du bien (fi)': {'width': 60},
                'Mode Gest (fi1)': {'title': _("Mode")},
                'Date de mise en service (fi)': {
                    'title': _("Date MES"),
                    'cell': {'num_format': 'MM/DD/YY'},
                },
                'Durée (fi2)': {'title': _("Durée Amort")},
                'DF Amort (fi2)': {
                    'title': _("Fin Amort"),
                    'cell': {'num_format': 'MM/DD/YY'},
                },
                'No UF (df)': {'title': _("UF")},
                'Libellé UF (df)': {'title': _("Libellé UF"), 'width': 50},
                'Qté UF (df1)': {'title': _("Qté UF")},
                'Répart. UF (df1)': {},
                'Répartition (fi1)': {},
                'Code Famille (fe)': {},
                'Libellé Famille (fe)': {'width': 50},
                'No Interne (fi)': {},
                'Actif UF (df2)': {'cell': {'num_format': '# ##0,00 [$€-40C];-# ##0,00 [$€-40C]'}},
                'note': {
                    'title': _("Commentaire"),
                    'width': 50,
                },
            },
        )
        dws.prepare()
        managed_cmd = set()
        managed_immo = set()
        for operation in previsionnel_qs:
            # op_row_data = model_to_dict(operation)
            op_row_data = {
                fname: getattr(operation, fname)
                for fname in (
                    'code_programme',
                    'num_dmd_id',
                    'libelle',
                    'budget',
                    'suivi_appro',
                    'suivi_mes',
                )
            }
            op_row_data['note'] = ''
            # Commandes citées dans le suivi appro
            commandes = set(
                map(
                    lambda s: s.upper(),
                    cmd_re.findall(operation.suivi_appro) if operation.suivi_appro else [],
                )
            )

            # Commandes dans les DRA associées
            dra_s = Dra94Dossier.objects.filter(programme=programme.anteriorite, ligne=operation.num_dmd_id)
            commandes |= set(instance.no_commande for instance in dra_s)

            if commandes:
                dfs = concat([commande_df[commande_df['no_commande'] == commande] for commande in commandes])
                if len(dfs):
                    for idx, row in dfs.iterrows():
                        cmd_row = op_row_data.copy()
                        cmd_row.update(row.to_dict())
                        immos = immobilisation_df[
                            (immobilisation_df['no_commande'] == str(row['no_commande']))
                            & (immobilisation_df['Ligne Commande (df)'] == int(row['No Ligne (lc)']))
                        ]
                        if len(immos):
                            for idx2, immo in immos.iterrows():
                                immo_row = cmd_row.copy()
                                immo_row.update(immo.to_dict())
                                if row['no_commande'] + '-' + str(row['No Ligne (lc)']) in managed_cmd:
                                    immo_row['Mt Engagé (lc)'] = 0
                                    immo_row['note'] += _("Ligne de commande déjà notée => engagé mis à 0 €. ")
                                else:
                                    managed_cmd.add(row['no_commande'] + '-' + str(row['No Ligne (lc)']))
                                if (
                                    '{:4d}-{:05d}'.format(
                                        immo_row['Exercice d\'acquisition (fi)'],
                                        immo_row['No Fiche (fi)'],
                                    )
                                    in managed_immo
                                ):
                                    immo_row['Actif UF (df2)'] = 0
                                    immo_row['note'] += _("Immobilisation déjà notée => actif mis à 0 €. ")
                                else:
                                    managed_immo.add(
                                        '{:4d}-{:05d}'.format(
                                            immo_row['Exercice d\'acquisition (fi)'],
                                            immo_row['No Fiche (fi)'],
                                        )
                                    )
                                dws.put_row(immo_row)
                        else:
                            if row['no_commande'] + '-' + str(row['No Ligne (lc)']) in managed_cmd:
                                cmd_row['Mt Engagé (lc)'] = 0
                                cmd_row['note'] += _("Ligne de commande déjà notée => engagé mis à 0 €. ")
                            else:
                                managed_cmd.add(row['no_commande'] + '-' + str(row['No Ligne (lc)']))
                            dws.put_row(cmd_row)

            else:
                op_row_data['note'] += _("Opération restant à traiter")
                dws.put_row(op_row_data)
        dws.finalize()

        wb.close()

        return ret_str
