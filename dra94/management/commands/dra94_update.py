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
import math
import os
import locale
import warnings
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.db.models import Min
from django.forms import model_to_dict
from django.utils import timezone
from django.utils.translation import gettext as _

from common import config
from dra94.models import Dra94Prevision, Dra94Dossier, Dra94Ligne
from drachar.models import Previsionnel

from tpsread.tpsread import TPS

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


def to_money(value):
    return float(value)


def to_code_uf(value):
    if value:
        return '{:04d}'.format(int(float(value)))


def to_no_reforme(value):
    if value:
        return "{:04d}/{:04d}".format(int(value) // 10000, int(value) % 10000)


def to_datetime(value):
    """Les dates sont stockées dans Clarion en nombre de jours depuis le 28/12/1800.
    Personne ne sait pourquoi."""
    return datetime(1800, 12, 28, tzinfo=timezone.utc) + timedelta(int(value))


def to_bool_from_str(value):
    if value:
        return {'OUI': True, 'NON': False}[value.upper()]


def get_tps_data(input_fn):
    tps = TPS(
        input_fn,
        encoding='iso8859-1',
        cached=True,
        check=True,
        current_tablename='UNNAMED',
    )
    records = []
    for record in tps:
        # remove 'XX:' prefix from keys
        rec = dict(zip([k.split(':')[1] for k in record.keys()], record.values()))
        # print(rec)
        records.append(rec)
        # if 'NUMERO' in rec and rec['NUMERO'] and int(rec['NUMERO']) in [20210157, 20210174, 20210206, 20210199]:
        #     print("    REC:", repr(rec))
    return records


def update_dra94_table(model, filename, fields_mapping):
    """Si nécessaire, lit le fichier TPS concerné et met à jour la table correspondante dans la BDD
    En fait, comme il n'y a pas de timestamp par enregistrement dans DRA94, la seule technique fiable est
    de vérifier la date de modification du fichier de DRA94 (= date de dernière mise à jour) et de refaire complètement
    la table si elle est antérieure à cette date. Pas très efficace..."""

    print("\nSynchronisation entre le fichier '{}' et la table <{}>".format(filename, str(model.__name__)))

    try:
        # Attention, on suppose ici que le filesystem a ses dates en UTC
        # (ce qui est le seul bon choix, mais qui n'est pas toujours vrai)
        mtime = datetime.fromtimestamp(os.stat(filename).st_mtime, tz=timezone.utc)
        print("  Fichier modifié le :", mtime)
    except FileNotFoundError:
        warnings.warn(f"Fichier {filename} non trouvé. Mise à jour ignorée.")
        return

    if model is not None:
        model_mtime = model.objects.all().values('date_creation').aggregate(Min('date_creation'))['date_creation__min']
        print("  Table Modifiée le  :", model_mtime)

        if model_mtime is None or model_mtime <= mtime:
            print("  => Import des données...")

            # Lecture des enregistrements dans Clarion / TPS
            print("    Lecture des données dans le fichier TPS Clarion...")
            records = get_tps_data(filename)
            print("      Enregistrements lus................. :", len(records))
            # dra94_fieldnames = list(records[0].keys())
            # print("  Champs :", dra94_fieldnames)
            # print("  Exemple :", repr(records[len(records) // 2]))
            # print("  Exemple :", repr(records[len(records) // 4]))
            # print("  Exemple :", repr(records[3 * len(records) // 4]))

            # Suppression complète valeurs de la table
            print("    Suppression enregistrements dans la table...")
            model.objects.all().delete()
            print("      Ok.")

            # Remplissage de la table avec les valeurs lues dans le TPS, en formatant si nécessaire
            print("    Remplissage de la table avec les données lues...")
            count = 0
            for s_record in records:
                values = {}
                # print("    record:", s_record)
                for fieldname in s_record.keys():
                    dest = fields_mapping[fieldname]['field']

                    # Corrige certaines entrées 'buggées' dans DRA94
                    if isinstance(s_record[fieldname], str) and '\0' in s_record[fieldname]:
                        s_record[fieldname] = ''

                    if 'fmt' in fields_mapping[fieldname]:
                        values[dest] = fields_mapping[fieldname]['fmt'](s_record[fieldname])
                    else:
                        values[dest] = s_record[fieldname]
                d_record = model(**values)
                d_record.save()
                count += 1
            print("      Enregistrements ajoutés dans la base : {}".format(count))
        else:
            print("  => Pas d'import.")


def update_dra94_tables():
    data_path = config.settings.DRA94_CFG['data_path']

    update_dra94_table(
        Dra94Prevision,
        os.path.join(data_path, 'prevision.tps'),
        {
            "RecNo'": {
                'field': 'record_no',
            },
            'PROGRAMME': {
                'field': 'programme',
            },
            'LIGNE': {
                'field': 'ligne',
                'fmt': int,
            },
            'SERVICE': {
                'field': 'service',
            },
            'CODEFAMILLE': {
                'field': 'code_famille',
            },
            'QUANTITEDMD': {
                'field': 'qte_demandee',
            },
            'INTITULE': {
                'field': 'intitule',
            },
            'QUANTITEACQ': {
                'field': 'qte_acquise',
                'fmt': int,
            },
            'COUTF': {
                'field': 'cout_francs',
                'fmt': to_money,
            },
            'COUTE': {
                'field': 'cout_euros',
                'fmt': to_money,
            },
            'REMARQUE': {
                'field': 'remarque',
            },
            'CELLULE': {
                'field': 'cellule',
            },
            'COUTREA': {
                'field': 'cout_realise',
            },
            'SOLDE': {
                'field': 'solde',
                'fmt': bool,
            },
            'UF': {
                'field': 'code_uf',
                'fmt': to_code_uf,
            },
        },
    )
    update_dra94_table(
        Dra94Dossier,
        os.path.join(data_path, 'DOSSIER.TPS'),
        {
            "RecNo'": {
                'field': 'record_no',
            },
            'NUMERO': {
                'field': 'numero',
                'fmt': int,
            },
            'DATEDOSSIER': {
                'field': 'date_dossier',
                'fmt': to_datetime,
            },
            'fourniss': {
                'field': 'fournisseur',
            },
            'codefouratelier': {
                'field': 'code_fournisseur',
                'fmt': int,
            },
            'point': {
                'field': 'point',
                'fmt': int,
            },
            'NOMSTE': {
                'field': 'contact_fournisseur',
            },
            'NDEVIS': {
                'field': 'numero_devis',
            },
            'DATEDEVIS': {
                'field': 'date_devis',
                'fmt': to_datetime,
            },
            'MONTANTE': {
                'field': 'montant',
                'fmt': to_money,
            },
            'codefamille': {
                'field': 'code_famille',
                'fmt': str,
            },
            'contact': {
                'field': 'contact',
            },
            'contactlivraison': {
                'field': 'contact_livraison',
            },
            'compte': {
                'field': 'numero_compte',
            },
            'UGAP': {
                'field': 'ugap',
            },
            'NPROG': {
                'field': 'programme',
            },
            'ligne': {
                'field': 'ligne',
            },
            'DIVERS': {
                'field': 'divers',
            },
            'dsio': {
                'field': 'dsio',
                'fmt': bool,
            },
            'transmis': {
                'field': 'date_transmission',
                'fmt': to_datetime,
            },
            'bon_commande': {
                'field': 'no_commande',
            },
            'datecde': {
                'field': 'date_commande',
                'fmt': to_datetime,
            },
            'fin_dossier': {
                'field': 'fin_dossier',
                'fmt': bool,
            },
            'cellule': {
                'field': 'cellule',
            },
            'n_marche': {
                'field': 'no_marche',
            },
            'imprime': {
                'field': 'imprime',
                'fmt': bool,
            },
            'piecejointe': {
                'field': 'pieces_jointes',
                'fmt': bool,
            },
        },
    )
    update_dra94_table(
        Dra94Ligne,
        os.path.join(data_path, 'ACHAT_new.TPS'),
        {
            "RecNo'": {
                'field': 'record_no',
                'fmt': int,
            },
            'DEPARTEMENT': {
                'field': 'departement',
            },
            'DATEDOSSIER': {
                'field': 'date_dossier',
                'fmt': to_datetime,
            },
            'TRI': {
                'field': 'tri',
            },
            'NUMERO': {
                'field': 'numero_dossier',
                'fmt': int,
            },
            'N_UF': {
                'field': 'code_uf',
                'fmt': to_code_uf,
            },
            'SURVEILLANT': {
                'field': 'cadre',
            },
            'DESIGN': {
                'field': 'designation',
            },
            'DESIGN_CNEH': {
                'field': 'designation_cneh',
            },
            'CNEH': {
                'field': 'code_cneh',
            },
            'SPECIFICITE': {
                'field': 'specificite',
            },
            'TYPE': {
                'field': 'type_modele',
            },
            'REFERENCE': {
                'field': 'reference',
            },
            'QTE': {
                'field': 'quantite',
            },
            'ACCESS': {
                'field': 'access',
            },
            'FOURNISS': {
                'field': 'fournisseur',
            },
            'NOMSTE': {
                'field': 'contact_fournisseur',
            },
            'EQUIP_RECUP': {
                'field': 'equipement_a_recuperer',
            },
            'MUTATION_REF': {
                'field': 'mutation_reforme',
            },
            'SERVICE': {
                'field': 'service',
            },
            'FORMATION': {
                'field': 'formation',
                'fmt': to_bool_from_str,
            },
            'VISITE_FIN_G': {
                'field': 'visite_fin_garantie',
                'fmt': to_bool_from_str,
            },
            'PTTCE': {
                'field': 'pu_ttc',
                'fmt': to_money,
            },
            'NUF_MUT': {
                'field': 'code_uf_mutation',
                'fmt': to_code_uf,
            },
            'SRV_MUT': {
                'field': 'service_mutation',
            },
            'SCT_MUT': {
                'field': 'sct_mutation',
            },
            'TOTALE': {
                'field': 'montant',
                'fmt': to_money,
            },
            'REFORME': {
                'field': 'numero_reforme',
                'fmt': to_no_reforme,
            },
            'DUREE_GARANTIE': {
                'field': 'duree_garantie',
                'fmt': int,
            },
            'JOUR_FORM': {
                'field': 'jours_formation',
                'fmt': int,
            },
            'SITE': {
                'field': 'site',
            },
            'DSIO': {
                'field': 'dsio',
                'fmt': float,
            },
            'DIRECTION': {
                'field': 'direction',
            },
            'RUBRIQUE': {
                'field': 'rubrique',
            },
            'ANNEERUB': {
                'field': 'annee_rubrique',
                'fmt': int,
            },
            'CHOIX': {
                'field': 'choix',
            },
            'MAINTENANCE_E': {
                'field': 'cout_maintenance',
            },
            'SUPPLEMENTAIRE': {
                'field': 'supplementaire',
                'fmt': to_bool_from_str,
            },
            'MARQUE': {
                'field': 'marque',
            },
            'REMISE': {
                'field': 'remise',
                'fmt': float,
            },
            'PUHTE': {
                'field': 'pu_ht',
                'fmt': to_money,
            },
            'GAIN': {
                'field': 'gain_ht',
            },
            'DATE_RECEPTION': {
                'field': 'date_reception',
                'fmt': to_datetime,
            },
            'DATE_SERVICE': {
                'field': 'date_mise_en_service',
                'fmt': to_datetime,
            },
            'RECU': {
                'field': 'recu',
                'fmt': to_bool_from_str,
            },
            'INSTALL': {
                'field': 'installe',
                'fmt': to_bool_from_str,
            },
            'TAUXTVA': {
                'field': 'taux_tva',
                'fmt': float,
            },
            'CONTRAT': {
                'field': 'contrat',
            },
            'CLASSE': {
                'field': 'classe',
            },
        },
    )


def update_previsionnel():
    for previsionnel in Previsionnel.objects.filter(programme__discipline__code='BM'):
        # print(previsionnel.programme.anteriorite, previsionnel.num_dmd.pk, previsionnel.budget)

        interface_html = "<ul>"

        previsionnels_dra94 = Dra94Prevision.objects.filter(
            programme=previsionnel.programme.anteriorite, ligne=previsionnel.num_dmd.pk
        )
        if previsionnels_dra94:
            previsionnel_dra94 = previsionnels_dra94.get()
            previsionnel_data = model_to_dict(previsionnel_dra94)

            # Quelques formattages & compléments
            previsionnel_data['enveloppe'] = locale.format_string(
                "%10.2f €",
                previsionnel_data['cout_euros'],
                grouping=True,
                monetary=True,
            )
            if math.fabs(float(previsionnel_data['cout_euros']) - float(previsionnel.budget)) > 0.01:
                previsionnel_data['err_montant'] = True
            else:
                previsionnel_data['err_montant'] = False

            # print(' ', previsionnel_data)
            tmpl = "<li>Prévisionnel DRA94 :<ul>"
            if previsionnel_data['err_montant']:
                tmpl += "<li style=\"background-color:#faa\">Montant : {enveloppe}</li>"
            else:
                tmpl += "<li>Montant : {enveloppe}</li>"
            if previsionnel_data['remarque']:
                tmpl += "<li>Remarque : {remarque}</li>"
            tmpl += "</ul></li>"
            interface_html += tmpl.format(**previsionnel_data)
        else:
            # print("  Pas de prévisionnel DRA94")
            interface_html += "<li>Pas de prévisionnel DRA94</li>"

        dra_list = Dra94Dossier.objects.filter(programme=previsionnel.programme.anteriorite, ligne=previsionnel.num_dmd.pk)
        montant_commande = 0
        if dra_list:
            for dra in dra_list:
                montant_commande += dra.montant
                dra_data = dict(
                    {
                        'dra': "DRA" + str(dra.numero)[:4] + "-" + str(dra.numero)[4:],
                        'montant_fr': locale.format_string("%10.2f €", dra.montant, grouping=True, monetary=True),
                    },
                    **model_to_dict(dra),
                )
                # print(' ', dra_data)

                tmpl = "<li>{dra}<ul>"
                tmpl += "<li>Montant : {montant_fr}</li>"
                if dra_data['no_commande']:
                    tmpl += "<li>Commande : {no_commande}</li>"
                tmpl += "</ul></li>"

                interface_html += tmpl.format(**dra_data)
        else:
            interface_html += "<li>Pas de DRA</li>"

        interface_html += "</ul>"

        previsionnel.interface = interface_html
        previsionnel.montant_commande = montant_commande
        previsionnel.save(update_fields=['montant_commande', 'interface'])


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(_("Mise à jour depuis DRA94..."))
        self.stdout.write(_("  Mise à jour des tables miroir de DRA94..."))
        update_dra94_tables()
        self.stdout.write(_("  Examen de Previsionnel..."))
        update_previsionnel()
        self.stdout.write(_("Mise à jour DRA94 terminée."))
