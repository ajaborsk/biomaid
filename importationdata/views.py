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
from assetplusconnect.views import ConnectorAssetPlus
from decimal import Decimal
from datetime import datetime

from common.models import Etablissement, Pole, CentreResponsabilite, Uf, Service, Site
from django.conf import settings
import csv  # TODO si pandas ok, modifier pour compte et supprimer cette biblio
import pandas as pd

from django.apps import apps
from django.db.models import Q

from django.utils import timezone
from django.db import transaction

from common.models import Discipline

'''
#/////////////////////////////////////////////////////////#
#               Fonction importation tables GMAO          #
#/////////////////////////////////////////////////////////#
'''


class BddImportation(ConnectorAssetPlus):
    """fonction d'intégration ou de mise à jour manuelle et automatique"""

    def import_data_gmao(self, *args, **kwargs):
        # importation des données d'une table liés avec ASSET+ sur commande manuelle
        """fonction qui récupère à partir des données du self : modele à traiter, le type_de_gmao,
        retourne le queryset correspondant et met à jour la table de BIOM_AID.0 correspondante"""
        if self.lien == 'ON':
            model = apps.get_model(
                app_label=self.app_bdd,
                model_name=settings.CORRESPONDANCEASSETPLUS[self.model.__name__],
            )
            m = model.records.using(self.bdd).all()  # queryset en attente de transaction
            return m

    def update_def(self, request, *args, **kwargs):
        # update des données d'une table liés avec ASSET+ sur commande manuelle
        '''Cette partie du code permet de réaliser les fonctions de mise a jour et enregistrement des tables
        en fonction des tables de la base de donnée d'Asset+ connectée dans le fichier config.ini'''
        '''######################################## CODE UPDATE TABLE MARQUE ########################################'''
        if self.bdd == "GMAO":
            if self.model_bdd == "assetplus":
                if self.version_bdd == "v10.8":
                    ConnectorAssetPlus.V10_8(self, request, BddImportation)
                else:
                    kwargs['message'] = "version d'asset plus non connue"
                    print(kwargs['message'])
                    pass
            elif self.model_bdd == 'optim':
                print("connecteur non encore créé")
                pass
            else:
                print("pas de GMAO désignée")
        elif self.bdd == "GEF":
            pass

    # @daily
    def daily_update(
        self,
    ):  # importation/update des données toutes les nuits des tables liés avec ASSET+
        # TODO : récupération des données de l'ensemble des données en liée avec ASSET+
        # TODO : utiliser l'outil JOBS de DJANGO_EXTENSION
        # déclenchement de la fonction sur les tables qui se voient modifiée dans common.model.updates_monitor
        pass


class FileImportation:
    ''''''

    def update_def(self, *args, **kwargs):
        if self.lien == 'FILE':
            if self.bdd == "GEF":
                if self.model_bdd == "magh2":
                    if self.version_bdd == "1.0":
                        # assurez vous que le fichier à importer est dans le repertoire "fixture",
                        # ait pour nom : " codeetablissement_GEF_nomtable_DATE.csv "
                        # TODO : import à finir
                        if self.model_update == "Compte":
                            start_time = timezone.now()
                            file_info = self.fichier.split("_")
                            etablissement_id = Etablissement.records.get(prefix=file_info[0])
                            fichier = 'fixtures/' + str(self.fichier)
                            with open(fichier, newline='') as csvfile:
                                filereader = csv.DictReader(
                                    csvfile,
                                    delimiter=';',
                                    fieldnames=(
                                        'lettre_budgetaire',
                                        'code',
                                        'nom',
                                        'exercice',
                                        'budget_montant',
                                        'discipline',
                                    ),
                                )
                                next(filereader)  # supprime la première ligne
                                """cas BDD non vide : mise a jour"""
                                # TODO : gérer cette notion de multi établissement et multifichier
                                if self.model.records.filter(etablissement=etablissement_id).exists():
                                    bdd_data = self.model.records.filter(etablissement=etablissement_id)
                                    for row in filereader:
                                        row["exercice"] = row["exercice"] + "-" + "01" + "-" + "01"
                                        for item in bdd_data:
                                            # instance = self.model.records.get(id=item.id)
                                            if (
                                                item.lettre_budgetaire == row["lettre_budgetaire"]
                                                and item.code == row["code"]
                                                and row["exercice"] == str(item.exercice)
                                            ):
                                                instance = self.model.records.get(id=item.id)
                                                if item.nom != row["nom"]:
                                                    instance.nom = row["nom"]
                                                if item.budget_montant != row["budget_montant"]:
                                                    instance.budget_montant = Decimal(row["budget_montant"])
                                                print(instance)
                                                instance.save()
                                                print(" l'item existe")
                                            # TODO /////////////////////////////////////////////////////////////////////
                                            # TODO : revoir cette condition qui ne convient pas :
                                            #       (croisement des deux FOR ne sont pas compléméntaires)
                                            else:
                                                if (
                                                    row["lettre_budgetaire"].lower() + row["code"]
                                                    in settings.COMPTEDISCPLINE.keys()
                                                ):
                                                    row["etablissement"] = etablissement_id
                                                    try:
                                                        discipline_id = Discipline.records.get(
                                                            code=settings.COMPTEDISCPLINE[
                                                                row["lettre_budgetaire"].lower() + row["code"]
                                                            ]
                                                        )
                                                    except Exception:
                                                        discipline_id = Discipline.records.get(code='XX')
                                                    row["discipline"] = discipline_id
                                                    print("exercice")
                                                    print(row["exercice"])
                                                    row["exercice"] = row["exercice"]
                                                    if row["budget_montant"] is None:
                                                        row["budget_montant"] = row["budget_montant"]
                                                    else:
                                                        print(row["budget_montant"])
                                                        row["budget_montant"] = Decimal(row["budget_montant"])
                                                    row = dict(row)
                                                    m = self.model(**row)
                                                    m.save()
                                                # TODO /////////////////////////////////////////////////////////////////
                                                # TODO : Checker à l'inverse si row existe dans item
                                    """cas BDD vide : first import"""
                                else:
                                    for row in filereader:
                                        if row["lettre_budgetaire"].lower() + row["code"] in settings.COMPTEDISCPLINE.keys():
                                            row["etablissement"] = etablissement_id
                                            try:
                                                discipline_id = Discipline.records.get(
                                                    code=settings.COMPTEDISCPLINE[row["lettre_budgetaire"].lower() + row["code"]]
                                                )
                                            except Exception:
                                                discipline_id = Discipline.records.get(code='XX')
                                            row["discipline"] = discipline_id
                                            row["exercice"] = row["exercice"]
                                            if row["budget_montant"] is None:
                                                row["budget_montant"] = row["budget_montant"]
                                            else:
                                                row["budget_montant"] = Decimal(row["budget_montant"])
                                            # print("budget2 : "+str(row["budget_montant"]))
                                            row = dict(row)
                                            m = self.model(**row)
                                            m.save()
                            elapsed_time = timezone.now() - start_time
                            print("elapsed_time : ")
                            print(elapsed_time)
                        # ________________________CODE D'IMPORTATION DE STRUCTURE_____________________#
                        if self.model_update == "structure":
                            """Code valable pour un CSV qui contient uniquement les UF ouvertes,
                            avec les données suivantes :
                            "code_etablisssement", "nom_etablissement", "code_uf",
                            "nom_uf_long", "budget", "cloture", "code_ccr", "nom_ccr",
                            "code_pole", "nom_pole_long", "code_service", "nom_service_long",
                            """
                            print("_____DEMARRAGE_____")
                            start_time = timezone.now()
                            print("start_time = " + str(start_time))
                            # file_info = self.fichier.split("_")
                            # etablissement_id = Etablissement.records.get(prefix=file_info[0])
                            etablissement_id = Etablissement.records.get(prefix=self.etabprefix)
                            fichier = str(self.fichier)

                            def code_converter(v):
                                """Ensure that the code is a string : If it's a integer, convert with {04d} format, if it's None, convert to ''"""
                                if isinstance(v, int):
                                    return '{:04d}'.format(v)
                                elif v is None:
                                    return ''
                                return v

                            data_csv = pd.read_csv(
                                fichier,
                                encoding='utf-8',
                                converters={
                                    'code_etablissement': code_converter,
                                    'code_service': code_converter,
                                    'code_site': code_converter,
                                    'code_pole': code_converter,
                                    'code_ccr': code_converter,
                                    'code_uf': code_converter,
                                },
                            )
                            d = timezone.now()
                            d.replace(year=d.year + 1)
                            data_csv['cloture'] = data_csv['cloture'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y'))
                            # pd.to_datetime(data_csv['cloture'], format='%d/%m/%Y')
                            df_data_csv = data_csv[(data_csv['cloture'] > d.replace(tzinfo=None))]
                            csv_pole = df_data_csv[['code_pole', 'nom_pole_long']].groupby('code_pole', as_index=False).first()
                            csv_cr = df_data_csv[['code_ccr', 'nom_ccr']].groupby('code_ccr', as_index=False).first()
                            csv_site = (
                                df_data_csv[["code_etablisssement", "nom_etablissement"]]
                                .groupby("code_etablisssement", as_index=False)
                                .first()
                            )
                            csv_service = (
                                df_data_csv[['code_service', 'nom_service_long']].groupby('code_service', as_index=False).first()
                            )
                            csv_uf = (
                                df_data_csv[
                                    [
                                        'code_uf',
                                        'nom_uf_long',
                                        'budget',
                                        "date_debut",
                                        "cloture",
                                        "code_etablisssement",
                                        "nom_etablissement",
                                        "code_service",
                                        "nom_service_long",
                                        "code_ccr",
                                        "nom_ccr",
                                        "code_pole",
                                        "nom_pole_long",
                                    ]
                                ]
                                .groupby('code_uf', as_index=False)
                                .first()
                            )
                            bdd_data_uf = Uf.records.filter(Q(etablissement=etablissement_id) & (Q(cloture=None)))
                            bdd_data_pole = Pole.records.filter(etablissement=etablissement_id, cloture=None)
                            bdd_data_cr = CentreResponsabilite.records.filter(etablissement=etablissement_id, cloture=None)
                            bdd_data_site = Site.records.filter(etablissement=etablissement_id, cloture=None)
                            bdd_data_service = Service.records.filter(etablissement=etablissement_id, cloture=None)
                            with transaction.atomic():
                                """#########check de la BDD SITE###########"""
                                """ ___________________Code de mise a jour et suppression dans la bdd_____________"""
                                if not bdd_data_site:  # cas ou la BDD est vierge ou Queryset vide, copie du CSV
                                    for element in csv_site.index:
                                        item = {}
                                        item["code"] = csv_site["code_etablisssement"][element]
                                        item["nom"] = csv_site["nom_etablissement"][element]
                                        item["etablissement"] = etablissement_id
                                        site = Site(**item)
                                        site.save()
                                else:
                                    found_row = []
                                    stop_transaction = False
                                    for row in bdd_data_site:  # dans un premier temps on compare la BDD au CSV
                                        # pour supprimer les manquants ou corrier les modifications
                                        with transaction.atomic():
                                            if stop_transaction is False:
                                                found_element = []
                                                for element in csv_site.index:
                                                    if row.code == csv_site["code_etablisssement"][element]:
                                                        if csv_site["nom_etablissement"][element] != row.nom:
                                                            row.nom = csv_site["nom_etablissement"][element]
                                                            row.save()
                                                        found_element = found_element + [
                                                            '{:04d}'.format(csv_site["code_etablisssement"][element])
                                                        ]
                                                """________________________test intégrité csv_______________________"""
                                                found_row = found_row + [row.code]
                                                if not found_element:  # suppression de la BDD car absent du CSV
                                                    instance = Site.records.get(id=row.id)
                                                    instance.cloture = timezone.now()
                                                    instance.save()
                                                # tests d'erreur elements du CSV
                                                elif len(found_element) >= 2:  # danger car doublon dans le CSV importé
                                                    stop_transaction = True
                                                    print("doublon dans le csv ATTENTION")
                                                    # TODO : produire l'alerte ou code
                                                    #    pour prendre le bon... ou mail à l'administrateur
                                                """_______________________test intégrité bdd_________________________"""
                                                # suppression en allant des doublons de la BDD
                                                if found_row.count(row.code) > 1:
                                                    deleted_id = (
                                                        Site.records.filter(
                                                            code=row.code,
                                                            etablissement_id=etablissement_id,
                                                            cloture=None,
                                                        )
                                                        .order_by('date_creation')
                                                        .first()
                                                        .id
                                                    )
                                                    s = Site.records.get(id=deleted_id)
                                                    s.cloture = timezone.now()
                                                    s.save()
                                                # tests d'erreur elements du CSV
                                                elif len(found_row) == 1:  # test a supprimmer à la fin
                                                    pass
                                    """ ___________________Code d'ajout dans la bdd_____________"""
                                    if stop_transaction is False:
                                        for element in csv_site.index:  # dans un second temps on compare le CSV à la BDD
                                            #   pour chercher les nouveaux élements
                                            found = False
                                            for row in bdd_data_site:
                                                if str(csv_site["code_etablisssement"][element]) == row.code:
                                                    found = True
                                            if not found:
                                                item = {}
                                                item["code"] = csv_site["code_etablisssement"][element]
                                                item["nom"] = csv_site["nom_etablissement"][element]
                                                item["etablissement"] = etablissement_id
                                                site = Site(**item)
                                                site.save()
                                """###########check de la BDD POLE###############"""
                                """ ___________________Code de mise a jour et suppression dans la bdd_____________"""
                                if not bdd_data_pole:  # cas ou la BDD est vierge ou Queryset vide, copie du CSV
                                    for element in csv_pole.index:
                                        item = {}
                                        item["code"] = csv_pole['code_pole'][element]
                                        item["nom"] = csv_pole['nom_pole_long'][element]
                                        item["etablissement"] = etablissement_id
                                        pole = Pole(**item)
                                        pole.save()
                                else:
                                    found_row = []
                                    for row in bdd_data_pole:  # dans un premier temps on compare la BDD au CSV
                                        # pour supprimer les manquants ou corrier les modifications
                                        found_element = []
                                        for element in csv_pole.index:
                                            if row.code == csv_pole['code_pole'][element]:
                                                if csv_pole['nom_pole_long'][element] != row.nom:
                                                    row.nom = csv_pole['nom_pole_long'][element]
                                                    row.save()
                                                found_element = found_element + [csv_pole['code_pole'][element]]
                                        """________________________test intégrité csv________________________________"""
                                        found_row = found_row + [row.code]
                                        if not found_element:  # suppression de la BDD car absent du CSV
                                            instance = Pole.records.get(id=row.id)
                                            instance.cloture = timezone.now()
                                            instance.save()
                                        # tests d'erreur elements du CSV
                                        elif len(found_element) >= 2:  # danger car doublon dans le CSV importé
                                            print("doublon dans le csv ATTENTION")
                                            # TODO : produire l'alerte ou code
                                            #   pour prendre le bon... ou mail à l'administrateur
                                        """_______________________test intégrité bdd_________________________"""
                                        # suppression en allant des doublons de la BDD
                                        if found_row.count(row.code) > 1:
                                            deleted_id = (
                                                Pole.records.filter(
                                                    code=row.code,
                                                    etablissement_id=etablissement_id,
                                                    cloture=None,
                                                )
                                                .order_by('date_creation')
                                                .first()
                                                .id
                                            )
                                            p = Pole.records.get(id=deleted_id)
                                            p.cloture = timezone.now()
                                            p.save()
                                        # tests d'erreur elements du CSV
                                        elif len(found_row) == 1:  # test a supprimmer à la fin
                                            pass
                                    """ ___________________Code d'ajout dans la bdd_____________"""
                                    for element in csv_pole.index:  # dans un second temps on compare le CSV à la BDD
                                        #   pour chercher les nouveaux élements
                                        found = False
                                        for row in bdd_data_pole:
                                            if str(csv_pole['code_pole'][element]) == row.code:
                                                found = True
                                        if not found:
                                            item = {}
                                            item["code"] = csv_pole['code_pole'][element]
                                            item["nom"] = csv_pole['nom_pole_long'][element]
                                            item["etablissement"] = etablissement_id
                                            pole = Pole(**item)
                                            pole.save()
                                    """#########check de la BDD CR###########"""
                                    """ ___________________Code de mise a jour et suppression dans la bdd____________"""
                                    if not bdd_data_cr:  # cas ou la BDD est vierge ou Queryset vide, copie du CSV
                                        for element in csv_cr.index:
                                            item = {}
                                            item["code"] = csv_cr['code_ccr'][element]
                                            item["nom"] = csv_cr['nom_ccr'][element]
                                            item["etablissement"] = etablissement_id
                                            cr = CentreResponsabilite(**item)
                                            cr.save()
                                    else:
                                        found_row = []
                                        for row in bdd_data_cr:  # dans un premier temps on compare la BDD au CSV
                                            #   pour supprimer les manquants ou corrier les modifications
                                            found_element = []
                                            for element in csv_cr.index:
                                                if row.code == csv_cr['code_ccr'][element]:
                                                    if csv_cr['nom_ccr'][element] != row.nom:
                                                        row.nom = csv_cr['nom_ccr'][element]
                                                        row.save()
                                                    found_element = found_element + [csv_cr['code_ccr'][element]]
                                            """________________________test intégrité csv____________________________"""
                                            found_row = found_row + [row.code]
                                            if not found_element:  # suppression de la BDD car absent du CSV
                                                instance = CentreResponsabilite.records.get(id=row.id)
                                                instance.cloture = timezone.now()
                                                instance.save()
                                            # tests d'erreur elements du CSV
                                            elif len(found_element) >= 2:  # danger car doublon dans le CSV importé
                                                print("doublon dans le csv ATTENTION")
                                                # TODO : produire l'alerte ou code
                                                #  pour prendre le bon... ou mail à l'administrateur
                                            """_______________________test intégrité bdd_________________________"""
                                            if found_row.count(row.code) > 1:
                                                # suppression en allant des doublons de la BDD
                                                deleted_id = (
                                                    CentreResponsabilite.records.filter(
                                                        code=row.code,
                                                        etablissement_id=etablissement_id,
                                                        cloture=None,
                                                    )
                                                    .order_by('date_creation')
                                                    .first()
                                                    .id
                                                )
                                                p = CentreResponsabilite.records.get(id=deleted_id)
                                                p.cloture = timezone.now()
                                                p.save()
                                            # tests d'erreur elements du CSV
                                            elif len(found_row) == 1:  # test a supprimmer à la fin
                                                pass
                                        """ ___________________Code d'ajout dans la bdd_____________"""
                                        for element in csv_cr.index:
                                            # dans un second temps on compare
                                            #   le CSV à la BDD pour chercher les nouveaux élements
                                            found = False
                                            for row in bdd_data_cr:
                                                if str(csv_cr['code_ccr'][element]) == row.code:
                                                    found = True
                                            if not found:
                                                item = {}
                                                item["code"] = csv_cr['code_ccr'][element]
                                                item["nom"] = csv_cr['nom_ccr'][element]
                                                item["etablissement"] = etablissement_id
                                                cr = CentreResponsabilite(**item)
                                                cr.save()
                                    """#########check de la BDD SERVICE###########"""
                                    """ __________________Code de mise a jour et suppression dans la bdd_____________"""
                                    if not bdd_data_service:  # cas ou la BDD est vierge ou Queryset vide, copie du CSV
                                        for element in csv_service.index:
                                            item = {}
                                            item["code"] = csv_service['code_service'][element]
                                            item["nom"] = csv_service['nom_service_long'][element]
                                            item["etablissement"] = etablissement_id
                                            cr = Service(**item)
                                            cr.save()
                                    else:
                                        found_row = []
                                        for row in bdd_data_service:  # dans un premier temps on compare la BDD au CSV
                                            #  pour supprimer les manquants ou corrier les modifications
                                            found_element = []
                                            for element in csv_service.index:
                                                if row.code == csv_service['code_service'][element]:
                                                    if csv_service['nom_service_long'][element] != row.nom:
                                                        row.nom = csv_service['nom_service_long'][element]
                                                        row.save()
                                                    found_element = found_element + [csv_service['code_service'][element]]
                                            """______________________test intégrité csv______________________________"""
                                            found_row = found_row + [row.code]
                                            if not found_element:  # suppression de la BDD car absent du CSV
                                                instance = Service.records.get(id=row.id)
                                                instance.cloture = timezone.now()
                                                instance.save()
                                            # tests d'erreur elements du CSV
                                            elif len(found_element) >= 2:  # danger car doublon dans le CSV importé
                                                print("doublon dans le csv ATTENTION")
                                                # TODO : produire l'alerte ou code
                                                #  pour prendre le bon... ou mail à l'administrateur
                                            """_______________________test intégrité bdd_________________________"""
                                            if found_row.count(row.code) > 1:
                                                # suppression en allant des doublons de la BDD
                                                deleted_id = (
                                                    Service.records.filter(
                                                        code=row.code,
                                                        etablissement_id=etablissement_id,
                                                        cloture=None,
                                                    )
                                                    .order_by('date_creation')
                                                    .first()
                                                    .id
                                                )
                                                p = Service.records.get(id=deleted_id)
                                                p.cloture = timezone.now()
                                                p.save()
                                            # tests d'erreur elements du CSV
                                            elif len(found_row) == 1:  # test a supprimmer à la fin
                                                pass
                                        """ ___________________Code d'ajout dans la bdd_____________"""
                                        for element in csv_service.index:  # dans un second temps on compare
                                            #  le CSV à la BDD pour chercher les nouveaux élements
                                            found = False
                                            for row in bdd_data_service:
                                                if str(csv_service['code_service'][element]) == row.code:
                                                    found = True
                                            if not found:
                                                item = {}
                                                item["code"] = csv_service['code_service'][element]
                                                item["nom"] = csv_service['nom_service_long'][element]
                                                item["etablissement"] = etablissement_id
                                                cr = Service(**item)
                                                cr.save()
                                    """#########check de la BDD UF###########"""
                                    """ ___________________Code de mise a jour et suppression dans la bdd____________"""
                                    if not bdd_data_uf:  # cas ou la BDD est vierge ou Queryset vide, copie du CSV
                                        for element in csv_uf.index:
                                            item = {}
                                            item["code"] = csv_uf['code_uf'][element]
                                            item["nom"] = csv_uf['nom_uf_long'][element]
                                            item["etablissement"] = etablissement_id
                                            item['lettre_budget'] = csv_uf['budget'][element]
                                            # TODO : créer une table des lettre Budgétaire ?
                                            #  ok, mais prévoir l modif de models + modif bdd actuelle
                                            item['site'] = Site.records.get(
                                                code=csv_uf["code_etablisssement"][element],
                                                etablissement_id=etablissement_id,
                                                cloture=None,
                                            )
                                            item['pole'] = Pole.records.get(
                                                code=csv_uf['code_pole'][element],
                                                etablissement_id=etablissement_id,
                                                cloture=None,
                                            )
                                            item['centre_responsabilite'] = CentreResponsabilite.records.get(
                                                code=csv_uf['code_ccr'][element],
                                                etablissement_id=etablissement_id,
                                                cloture=None,
                                            )
                                            item['service'] = Service.records.get(
                                                code=csv_uf['code_service'][element],
                                                etablissement_id=etablissement_id,
                                                cloture=None,
                                            )
                                            if csv_uf["cloture"][element] <= timezone.now().replace(
                                                tzinfo=None
                                            ):  # si la date de fin de l'UF est inférieur
                                                #  à date du jour + 1 an => l'UF est enore ouverte
                                                item['cloture'] = csv_uf["cloture"][element]
                                            elif str(csv_uf["nom_uf_long"][element]).casefold()[:2] == "xx" and not row.cloture:
                                                item['cloture'] = timezone.now()
                                            uf = Uf(**item)
                                            uf.save()
                                    else:
                                        found_row = []
                                        for row in bdd_data_uf:  # dans un premier temps on compare la BDD au CSV
                                            # pour supprimer les manquants ou corrier les modifications
                                            found_element = []
                                            for element in csv_uf.index:
                                                if row.code == csv_uf['code_uf'][element]:
                                                    if csv_uf["cloture"][element] <= timezone.now().replace(tzinfo=None):
                                                        row.cloture = csv_uf["cloture"][element]
                                                        row.save()
                                                    elif (
                                                        str(csv_uf["nom_uf_long"][element]).casefold()[:2] == "xx"
                                                        and not row.cloture
                                                    ):  # or str(csv_uf["nom_uf_long"][element])[:2] == "XX":
                                                        row.cloture = timezone.now()
                                                        if csv_uf['nom_uf_long'][element] != row.nom:
                                                            row.nom = csv_uf['nom_uf_long'][element]
                                                        row.save()
                                                    else:
                                                        if csv_uf['nom_uf_long'][element] != row.nom:
                                                            row.nom = csv_uf['nom_uf_long'][element]
                                                            row.save()
                                                        if csv_uf['budget'][element] != row.lettre_budget:
                                                            row.lettre_budget = csv_uf['budget'][element]
                                                            row.save()
                                                        if csv_uf["code_etablisssement"][element] != row.site:
                                                            row.site = Site.records.get(
                                                                code=csv_uf["code_etablisssement"][element],
                                                                etablissement_id=etablissement_id,
                                                                cloture=None,
                                                            )
                                                            row.save()
                                                        if csv_uf["code_pole"][element] != row.pole:
                                                            row.pole = Pole.records.get(
                                                                code=csv_uf["code_pole"][element],
                                                                etablissement_id=etablissement_id,
                                                                cloture=None,
                                                            )
                                                            row.save()
                                                        if csv_uf["code_ccr"][element] != row.centre_responsabilite:
                                                            row.centre_responsabilite = CentreResponsabilite.records.get(
                                                                code=csv_uf["code_ccr"][element],
                                                                etablissement_id=etablissement_id,
                                                                cloture=None,
                                                            )
                                                            row.save()
                                                        if csv_uf["code_service"][element] != row.service:
                                                            row.service = Service.records.get(
                                                                code=csv_uf["code_service"][element],
                                                                etablissement_id=etablissement_id,
                                                                cloture=None,
                                                            )
                                                            row.save()
                                                    found_element = found_element + [csv_uf['code_uf'][element]]
                                            """______________________test intégrité csv______________________________"""
                                            found_row = found_row + [row.code]
                                            if not found_element:  # suppression de la BDD car absent du CSV
                                                instance = Uf.records.get(id=row.id)
                                                instance.cloture = timezone.now()
                                                instance.save()
                                            # tests d'erreur elements du CSV
                                            elif len(found_element) >= 2:  # danger car doublon dans le CSV importé
                                                print("doublon dans le csv ATTENTION")
                                                # TODO : produire l'alerte ou code
                                                #  pour prendre le bon... ou mail à l'administrateur
                                            """_______________________test intégrité bdd_________________________"""
                                            if found_row.count(row.code) > 1:
                                                # suppression en allant des doublons de la BDD
                                                deleted_id = (
                                                    Uf.records.filter(
                                                        code=row.code,
                                                        etablissement_id=etablissement_id,
                                                        cloture=None,
                                                    )
                                                    .order_by('date_creation')
                                                    .first()
                                                    .id
                                                )
                                                p = Uf.records.get(id=deleted_id)
                                                p.cloture = timezone.now()
                                                p.save()
                                            # tests d'erreur elements du CSV
                                            elif len(found_row) == 1:  # test a supprimmer à la fin
                                                pass
                                        """ ___________________Code d'ajout dans la bdd_____________"""
                                        for element in csv_uf.index:  # dans un second temps on compare
                                            # le CSV à la BDD pour chercher les nouveaux élements
                                            found = False
                                            for row in bdd_data_uf:
                                                if str(csv_uf['code_uf'][element]) == row.code:
                                                    found = True
                                            if not found and (
                                                str(csv_uf["nom_uf_long"][element]).casefold()[:2] != "xx"
                                                or csv_uf["cloture"][element] < timezone.now().replace(tzinfo=None)
                                            ):
                                                item = {}
                                                item["code"] = csv_uf['code_uf'][element]
                                                item["nom"] = csv_uf['nom_uf_long'][element]
                                                item["etablissement"] = etablissement_id
                                                item['lettre_budget'] = csv_uf['budget'][element]
                                                # TODO : créer une table des lettre Budgétaire ?
                                                #  ok, mais prévoir l modif de models + modif bdd actuelle
                                                item['site'] = Site.records.get(
                                                    code=csv_uf["code_etablisssement"][element],
                                                    etablissement_id=etablissement_id,
                                                    cloture=None,
                                                )
                                                item['pole'] = Pole.records.get(
                                                    code=csv_uf['code_pole'][element],
                                                    etablissement_id=etablissement_id,
                                                    cloture=None,
                                                )
                                                item['centre_responsabilite'] = CentreResponsabilite.records.get(
                                                    code=csv_uf['code_ccr'][element],
                                                    etablissement_id=etablissement_id,
                                                    cloture=None,
                                                )
                                                item['service'] = Service.records.get(
                                                    code=csv_uf['code_service'][element],
                                                    etablissement_id=etablissement_id,
                                                    cloture=None,
                                                )
                                                if csv_uf["cloture"][element] > timezone.now().replace(tzinfo=None):
                                                    item['cloture'] = None
                                                elif csv_uf["cloture"][element] <= timezone.now().replace(
                                                    tzinfo=None
                                                ):  # si la date de fin de l'UF est inférieure
                                                    # à date du jour + 1 an => l'UF est encore ouverte
                                                    item['cloture'] = csv_uf["cloture"][element]
                                                elif str(csv_uf["nom_uf_long"][element]).casefold()[:2] == "xx" and not row.cloture:
                                                    row.cloture = timezone.now()
                                                    if csv_uf['nom_uf_long'][element] != row.nom:
                                                        row.nom = csv_uf['nom_uf_long'][element]
                                                uf = Uf(**item)
                                                uf.save()
                                    """______________________________________________________________________________"""
                                elapsed_time = timezone.now() - start_time
                                print("elapsed_time : " + str(elapsed_time))
                                print("_____FIN_____")
                                pass
                    else:
                        kwargs['message'] = "version de magh2 plus non connue"
                        print(kwargs['message'])
                        pass
                else:
                    kwargs['message'] = "pas de gef renseignée"
                    print(kwargs['message'])
                    pass
            else:
                pass
