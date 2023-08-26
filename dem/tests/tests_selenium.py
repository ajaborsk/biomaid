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
import json
import os
import time
import urllib.parse

import time_machine
from django.urls import reverse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from parameterized import parameterized

from common import config
from common.tests.tests_selenium import TestsBaseTestCase
from dem.models import Demande, Campagne
from document.models import Document

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep + os.path.join(BASE_DIR, '/gecko')


class TestsBaseTests(TestsBaseTestCase):
    @parameterized.expand(
        [
            ('dem:aide',),
            ('dem:home',),
            (
                'dem:request-create',
                {},
                '?' + urllib.parse.urlencode({'choices': json.dumps({'calendrier': [1]})}),
            ),
            ('dem:demandes-en-cours',),
            ('drachar:suivi-plans',),
            ('dem:demandes-tout',),
        ]
    )
    def test_pages_with_login(self, url_name, url_kwargs=None, url_parameters=''):
        url_kwargs = url_kwargs or {}
        """Pages nécessitant d'être connecté"""
        url = reverse(url_name, kwargs=dict(self.reverse_base, **url_kwargs)) + url_parameters
        self.login()
        self.selenium.get("{}{}".format(self.live_server_url, url))
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)


class TestsUser1(TestsBaseTestCase):
    def setUp(self):
        super().setUp()
        self.login()

    @time_machine.travel("2020-09-12 18:00 +0000")
    def test_saisie_demande_minimale(self):
        "Saisie d'une demande minimale"
        # On va sur la page pour faire une demande
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse(
                    'dem:request-create',
                    # kwargs=dict(self.reverse_base, **{'campagne_code': 'TEST'}),
                    kwargs=self.reverse_base,
                )
                + '?'
                + urllib.parse.urlencode({'choices': json.dumps({'calendrier': [Campagne.records.get(code='TEST').pk]})}),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        # Saisie du strict minimum :
        #  UF
        self.selenium.find_element(by=By.ID, value="id_request_table-uf-flexdatalist").send_keys('0001')
        time.sleep(0.5)
        self.selenium.find_element(by=By.ID, value="id_request_table-uf-flexdatalist").send_keys(Keys.DOWN, Keys.ENTER)

        #  Référent
        self.selenium.find_element(by=By.ID, value="id_request_table-referent").send_keys('Moi-même\t')
        #  Objet de la demande
        self.selenium.find_element(by=By.ID, value="id_request_table-libelle").send_keys('Equipement\t')

        # Enregistre la demande
        save_button = self.selenium.find_elements(by=By.CSS_SELECTOR, value='[value="record"]')[0]
        save_button.click()

        self.assertIn(
            "enregistré",
            self.selenium.find_elements(by=By.CLASS_NAME, value="dialog-message")[0].text,
        )

        # Click ok sur la boîte de dialogue
        self.selenium.find_element(by=By.ID, value='main-dialog-ok').click()

        # Vérifie qu'il n'y a pas d'erreur ensuite
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

    @time_machine.travel("2020-02-02 21:00 +0000")
    def test_saisie_demande_avant(self):
        "Saisie d'une demande avant le début de la campagne"

        nb_dmd = Demande.records.all().count()

        # On va sur la page pour faire une demande
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse(
                    'dem:request-create',
                    kwargs=self.reverse_base,
                )
                + '?'
                + urllib.parse.urlencode({'choices': json.dumps({'calendrier': [Campagne.records.get(code='TEST').pk]})}),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        # Vérification alerte campagne non ouverte
        self.assertIn(
            "ne pouvez pas",
            self.selenium.find_element(by=By.ID, value="exception-message").text,
        )

        # # Ferme la boîte de dialogue
        # self.selenium.find_element(by=By.ID, value='main-dialog-ok').click()
        #
        # # Saisie du strict minimum :
        # #  UF
        # self.selenium.find_element(by=By.ID, value="id_request_table-uf-flexdatalist").send_keys('0001')
        # time.sleep(0.2)
        # self.selenium.find_element(by=By.ID, value="idrequest_table-uf-flexdatalist").send_keys(Keys.DOWN, Keys.ENTER)
        #
        # #  Référent
        # self.selenium.find_element(by=By.ID, value="id_request_table-referent").send_keys('Moi-même\t')
        # #  Objet de la demande
        # self.selenium.find_element(by=By.ID, value="id_request_table-libelle").send_keys('Equipement\t')
        #
        # # Enregistre la demande
        # save_button = self.selenium.find_elements(by=By.CSS_SELECTOR, value='#form input[name="submit"]')[0]
        # save_button.click()
        #
        # self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)
        #
        # # Vérification alerte campagne non ouverte
        # self.assertIn(
        #     "campagne de recensement est close",
        #     self.selenium.find_element(by=By.ID, value="main-help").text,
        # )

        # Vérification qu'aucun enregistrement de demande n'a été fait
        self.assertEqual(nb_dmd, Demande.records.all().count())

    @time_machine.travel("2021-01-02 09:00 +0000")
    def test_saisie_demande_apres(self):
        "Saisie d'une demande après la fin de la campagne"

        nb_dmd = Demande.records.all().count()
        # print("Demandes dans la base avant:", nb_dmd)

        # On va sur la page pour faire une demande
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse(
                    'dem:request-create',
                    kwargs=self.reverse_base,
                )
                + '?'
                + urllib.parse.urlencode({'choices': json.dumps({'calendrier': [Campagne.records.get(code='TEST').pk]})}),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        # Vérification alerte campagne non ouverte
        self.assertIn(
            "ne pouvez pas",
            self.selenium.find_element(by=By.ID, value="exception-message").text,
        )

        # # Vérification alerte campagne non ouverte
        # self.assertIn(
        #     "campagne de recensement close",
        #     self.selenium.find_element(by=By.ID, value="main-help").text,
        # )
        #
        # # Ferme la boîte de dialogue
        # self.selenium.find_element(by=By.ID, value='main-dialog-ok').click()
        #
        # # Saisie du strict minimum :
        # #  UF
        # self.selenium.find_element(by=By.ID, value="id_request_table-uf-flexdatalist").send_keys('0001')
        # time.sleep(0.2)
        # self.selenium.find_element(by=By.ID, value="id_request_table-uf-flexdatalist").send_keys(Keys.DOWN, Keys.ENTER)
        #
        # #  Référent
        # self.selenium.find_element(by=By.ID, value="id_request_table-referent").send_keys('Moi-même\t')
        # #  Objet de la demande
        # self.selenium.find_element(by=By.ID, value="id_request_table-libelle").send_keys('Equipement\t')
        #
        # # Enregistre la demande
        # save_button = self.selenium.find_elements(by=By.CSS_SELECTOR, value='#form input[name="submit"]')[0]
        # save_button.click()
        #
        # self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)
        #
        # # Vérification alerte campagne non ouverte
        # self.assertIn(
        #     "campagne de recensement est close",
        #     self.selenium.find_element(by=By.ID, value="main-help").text,
        # )

        # Vérification qu'aucun enregistrement de demande n'a été fait
        print("Demandes dans la base après:", Demande.records.all().count())
        self.assertEqual(nb_dmd, Demande.records.all().count())

    @time_machine.travel("2020-09-12 18:00 +0000")
    def test_saisie_demande_complete(self):
        "Saisie d'une demande complete"
        # On va sur la page pour faire une demande
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse(
                    'dem:request-create',
                    kwargs=self.reverse_base,
                )
                + '?'
                + urllib.parse.urlencode({'choices': json.dumps({'calendrier': [Campagne.records.get(code='TEST').pk]})}),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        # Saisie du strict minimum :
        #  UF
        self.selenium.find_element(by=By.ID, value="id_request_table-uf-flexdatalist").send_keys('0001')
        time.sleep(0.5)
        self.selenium.find_element(by=By.ID, value="id_request_table-uf-flexdatalist").send_keys(Keys.DOWN, Keys.ENTER)

        #  Référent
        self.selenium.find_element(by=By.ID, value="id_request_table-referent").send_keys('Moi-même')
        #  Objet de la demande
        self.selenium.find_element(by=By.ID, value="id_request_table-libelle").send_keys('Equipement')

        #  Quantité (DELETE + valeur)
        self.selenium.find_element(by=By.ID, value="id_request_table-quantite").send_keys(Keys.DELETE + '3')

        #  Prix unitaire
        self.selenium.find_element(by=By.ID, value="id_request_table-prix_unitaire").send_keys('10000')

        # to change focus without doing anything
        self.selenium.find_element(by=By.ID, value="id_request_table-referent").send_keys('')
        time.sleep(0.01)

        # Mise en forme du prix unitaire ?
        self.assertEqual(
            self.selenium.find_element(by=By.ID, value="id_request_table-prix_unitaire").get_attribute('value'),
            '10\u202f000 €',
        )

        # -------------------------------------------------------------------------------------------------------------------------
        # Insertion d'un document

        # Saisie du code
        self.selenium.find_element(by=By.ID, value="id_document-genericdocument-content_type-object_id-0-document_type").send_keys(
            Keys.DOWN, Keys.DOWN, Keys.DOWN, Keys.TAB
        )

        # Saisie du nom du fichier. Il faut impérativement utiliser un chemin absolu car on ne fait pas de choix dans une boîte
        self.selenium.find_element(by=By.ID, value="id_document-genericdocument-content_type-object_id-0-document_file").send_keys(
            os.path.abspath('.') + '/fixtures/tests_db.json'
        )

        self.selenium.find_element(
            by=By.ID, value="id_document-genericdocument-content_type-object_id-0-document_comment"
        ).send_keys("document joint pour test")

        # -------------------------------------------------------------------------------------------------------------------------

        # Enregistre la demande
        save_button = self.selenium.find_elements(by=By.CSS_SELECTOR, value='[value="record"]')[0]
        save_button.click()

        self.assertIn(
            "enregistré",
            self.selenium.find_elements(by=By.CLASS_NAME, value="dialog-message")[0].text,
        )

        # Click ok sur la boîte de dialogue
        self.selenium.find_element(by=By.ID, value='main-dialog-ok').click()

        # Vérifie qu'il n'y a pas d'erreur ensuite
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        document_records = Document.records.filter().values()
        self.assertEqual(len(document_records), 1)
        document_record = document_records[0]

        self.assertEqual(document_record['doc_type'], "IM")  # Image (photo) is the fourth in the list (3 times key down)
        self.assertEqual(document_record['description'], "document joint pour test")

    def test_avis_cadre_sup(self):
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse('dem:demandes-en-cours', kwargs=self.reverse_base),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'avis_cadre_sup',
        )

        # La case est bien présente
        self.assertIsNotNone(cell)

        # Doit être non coché (base de tests)
        self.assertIn(
            'fa-circle',
            cell.find_elements(by=By.CLASS_NAME, value='fa-regular')[0].get_attribute('class'),
        )

        cell.click()

        # Ne doit pas avoir changé !
        time.sleep(0.1)
        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'avis_cadre_sup',
        )
        self.assertIn(
            'fa-circle',
            cell.find_elements(by=By.CLASS_NAME, value='fa-regular')[0].get_attribute('class'),
        )

    def test_commentaire_cadre_pole(self):
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse('dem:demandes-en-cours', kwargs=self.reverse_base),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'commentaire_cadre_sup',
        )

        # La case est bien présente
        self.assertIsNotNone(cell)

        # Cela doit normalement créer le champ éditable
        cell.click()

        # On saisit un avis
        textareas = cell.find_elements(by=By.TAG_NAME, value="textarea")

        self.assertEqual(len(textareas), 0, "Il y a au moins un champs éditable...")

        # On clique n'importe où sur la page pour valider la saisie
        self.selenium.find_element(by=By.TAG_NAME, value='body').click()

    def test_validation_chef_pole(self):
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse('dem:demandes-en-cours', kwargs=self.reverse_base),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'decision_validateur',
        )

        # La case est bien présente
        self.assertIsNotNone(cell)

        # Doit être non coché (base de tests)
        self.assertIn(
            'fa-circle',
            cell.find_elements(by=By.CLASS_NAME, value='fa-regular')[0].get_attribute('class'),
        )

        cell.click()

        # Ne doit pas avoir changé !
        time.sleep(0.1)
        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'decision_validateur',
        )
        self.assertIn(
            'fa-circle',
            cell.find_elements(by=By.CLASS_NAME, value='fa-regular')[0].get_attribute('class'),
        )

    def test_commentaire_chef_pole(self):
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse('dem:demandes-en-cours', kwargs=self.reverse_base),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'decision_soumission',
        )

        # La case est bien présente
        self.assertIsNotNone(cell)

        # Cela doit normalement créer le champ éditable
        cell.click()

        # On saisit un avis
        textareas = cell.find_elements(by=By.TAG_NAME, value="textarea")

        self.assertEqual(len(textareas), 0, "Il y a au moins un champs éditable...")

        # On clique n'importe où sur la page pour valider la saisie
        self.selenium.find_element(by=By.TAG_NAME, value='body').click()


class TestsCadrePole(TestsBaseTestCase):
    def setUp(self):
        super().setUp()
        self.login('enbaveyv')

    def test_avis_cadre_sup(self):
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse('dem:demandes-en-cours', kwargs=self.reverse_base),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'avis_cadre_sup',
        )

        # La case est bien présente
        self.assertIsNotNone(cell)

        # Doit être non coché (base de tests)
        self.assertIn(
            'fa-circle',
            cell.find_elements(by=By.CLASS_NAME, value='fa-regular')[0].get_attribute('class'),
        )

        cell.click()
        # Doit avoir changé (checked) !
        time.sleep(0.1)
        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'avis_cadre_sup',
        )
        self.assertIn(
            'fa-check',
            cell.find_elements(by=By.CLASS_NAME, value='fa-solid')[0].get_attribute('class'),
        )

        # Vérification que la base a bien été mise à jour
        demande = Demande.records.get(pk=1)
        self.assertTrue(demande.avis_cadre_sup)

        cell.click()
        # Doit avoir changé (cross) !
        time.sleep(1)
        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'avis_cadre_sup',
        )
        self.assertIn(
            'fa-xmark',
            cell.find_elements(by=By.CLASS_NAME, value='fa-solid')[0].get_attribute('class'),
        )

        # Vérification que la base a bien été mise à jour
        demande = Demande.records.get(pk=1)
        self.assertFalse(demande.avis_cadre_sup)

        cell.click()
        # Doit avoir changé (retour à l'état sans avis) !
        time.sleep(1)
        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'avis_cadre_sup',
        )
        self.assertIn(
            'fa-circle',
            cell.find_elements(by=By.CLASS_NAME, value='fa-regular')[0].get_attribute('class'),
        )

        # Vérification que la base a bien été mise à jour
        demande = Demande.records.get(pk=1)
        self.assertIsNone(demande.avis_cadre_sup)

    def test_commentaire_cadre_pole(self):
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse('dem:demandes-en-cours', kwargs=self.reverse_base),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'commentaire_cadre_sup',
        )

        # La case est bien présente
        self.assertIsNotNone(cell)

        # Cela doit normalement créer le champ éditable
        cell.click()

        # On saisit un avis
        cell.find_element(by=By.TAG_NAME, value="textarea").send_keys("Avis tout à fait favorable")

        # On clique n'importe où sur la page pour valider la saisie
        self.selenium.find_element(by=By.TAG_NAME, value='body').click()

        # Vérification que la base a bien été mise à jour
        time.sleep(0.1)
        demande = Demande.records.get(pk=1)
        self.assertEqual(demande.commentaire_cadre_sup, "Avis tout à fait favorable")

    def test_validation_chef_pole(self):
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse('dem:demandes-en-cours', kwargs=self.reverse_base),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'decision_validateur',
        )

        # La case est bien présente
        self.assertIsNotNone(cell)

        # Doit être non coché (base de tests)
        self.assertIn(
            'fa-circle',
            cell.find_elements(by=By.CLASS_NAME, value='fa-regular')[0].get_attribute('class'),
        )

        cell.click()

        # Ne doit pas avoir changé !
        time.sleep(1)
        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'decision_validateur',
        )
        self.assertIn(
            'fa-circle',
            cell.find_elements(by=By.CLASS_NAME, value='fa-regular')[0].get_attribute('class'),
        )

    def test_commentaire_chef_pole(self):
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse('dem:demandes-en-cours', kwargs=self.reverse_base),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'decision_soumission',
        )

        # La case est bien présente
        self.assertIsNotNone(cell)

        # Cela doit normalement créer le champ éditable
        cell.click()

        # On saisit un avis
        textareas = cell.find_elements(by=By.TAG_NAME, value="textarea")

        self.assertEqual(len(textareas), 0, "Il y a au moins un champs éditable...")

        # On clique n'importe où sur la page pour valider la saisie
        self.selenium.find_element(by=By.TAG_NAME, value='body').click()


class TestsChefPole(TestsBaseTestCase):
    def setUp(self):
        super().setUp()
        self.login('cekilesy')

    def test_avis_cadre_sup(self):
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse('dem:demandes-en-cours', kwargs=self.reverse_base),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'avis_cadre_sup',
        )

        # La case est bien présente
        self.assertIsNotNone(cell)

        # Doit être non coché (base de tests)
        self.assertIn(
            'fa-circle',
            cell.find_elements(by=By.CLASS_NAME, value='fa-regular')[0].get_attribute('class'),
        )

        cell.click()

        # Ne doit pas avoir changé !
        time.sleep(0.1)
        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'avis_cadre_sup',
        )
        self.assertIn(
            'fa-circle',
            cell.find_elements(by=By.CLASS_NAME, value='fa-regular')[0].get_attribute('class'),
        )

    def test_commentaire_cadre_pole(self):
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse('dem:demandes-en-cours', kwargs=self.reverse_base),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'commentaire_cadre_sup',
        )

        # La case est bien présente
        self.assertIsNotNone(cell)

        # Cela doit normalement créer le champ éditable
        cell.click()

        # On saisit un avis
        textareas = cell.find_elements(by=By.TAG_NAME, value="textarea")

        self.assertEqual(len(textareas), 0, "Il y a au moins un champs éditable...")

        # On clique n'importe où sur la page pour valider la saisie
        self.selenium.find_element(by=By.TAG_NAME, value='body').click()

    def test_validation_chef_pole(self):
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse('dem:demandes-en-cours', kwargs=self.reverse_base),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'decision_validateur',
        )

        # La case est bien présente
        self.assertIsNotNone(cell)

        # Doit être non coché (base de tests)
        self.assertIn(
            'fa-circle',
            cell.find_elements(by=By.CLASS_NAME, value='fa-regular')[0].get_attribute('class'),
        )

        cell.click()
        # Doit avoir changé (checked) !
        time.sleep(0.1)
        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'decision_validateur',
        )
        self.assertIn(
            'fa-check',
            cell.find_elements(by=By.CLASS_NAME, value='fa-solid')[0].get_attribute('class'),
        )

        # Vérification que la base a bien été mise à jour
        demande = Demande.records.get(pk=1)
        self.assertTrue(demande.decision_validateur)

        cell.click()
        # Doit avoir changé (cross) !
        time.sleep(1)
        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'decision_validateur',
        )
        self.assertIn(
            'fa-xmark',
            cell.find_elements(by=By.CLASS_NAME, value='fa-solid')[0].get_attribute('class'),
        )

        # Vérification que la base a bien été mise à jour
        demande = Demande.records.get(pk=1)
        self.assertFalse(demande.decision_validateur)

        cell.click()
        # Doit avoir changé (retour à l'état sans avis) !
        time.sleep(0.1)
        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'decision_validateur',
        )
        self.assertIn(
            'fa-circle',
            cell.find_elements(by=By.CLASS_NAME, value='fa-regular')[0].get_attribute('class'),
        )

        # Vérification que la base a bien été mise à jour
        demande = Demande.records.get(pk=1)
        self.assertIsNone(demande.decision_validateur)

    def test_commentaire_chef_pole(self):
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse('dem:demandes-en-cours', kwargs=self.reverse_base),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        cell = self.get_tabulator_cell(
            'demandes_en_cours_table-smart-view-table',
            'code',
            'DEM-2021-00000',
            'decision_soumission',
        )

        # La case est bien présente
        self.assertIsNotNone(cell)

        # Cela doit normalement créer le champ éditable
        cell.click()

        # On saisit un avis
        cell.find_element(by=By.TAG_NAME, value="textarea").send_keys("Avis tout à fait favorable")

        # On clique n'importe où sur la page pour valider la saisie
        self.selenium.find_element(by=By.TAG_NAME, value='body').click()

        # Vérification que la base a bien été mise à jour
        time.sleep(0.1)
        demande = Demande.records.get(pk=1)
        self.assertEqual(demande.decision_soumission, "Avis tout à fait favorable")


class TestsAcheteur(TestsBaseTestCase):
    def setUp(self):
        super().setUp()
        self.login('timettvi')

    def test_expert_vue_demandes(self):
        "Affichage du tableau des demandes comme expert"

        # On va sur la page des experts
        self.selenium.get("{}{}".format(self.live_server_url, reverse('dem:expertise', kwargs=self.reverse_base)))

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

    CHK_FIELDS = [
        'date',
        'nom_projet',
        'redacteur',
        # 'nom_cadre_sup',
        # 'avis_cadre_sup',
        # 'commentaire_cadre_sup',
        # 'validateur',
        # 'decision_validateur',
        # 'decision_soumission',
        'uf',
        'nom_organisation',
        'code_pole',
        'nom_pole_court',
        'code_uf',
        'nom_uf_court',
        'referent',
        'contact',
        'dect_contact',
        'date_premiere_demande',
        'priorite',
        'libelle',
        'cause',
        'materiel_existant',
        'quantite',
        'prix_unitaire',
        'couts_complementaires',
        'autre_argumentaire',
        # 'montant',
        'consommables_eventuels',
        'impact_travaux',
        'impact_informatique',
    ]

    @parameterized.expand([(fname, 2, [fname]) for fname in CHK_FIELDS])
    def test_avis_expert_modif_demande(self, name, pk, fields):
        "L'ajout d'un avis d'expert ne modifie pas la demande originale"

        # On stocke dans une variable les champs spécifiés de la demande AVANT modification
        demande = Demande.records.get(pk=pk)
        demande_before = {fieldname: demande._meta.get_field(fieldname).value_to_string(demande) for fieldname in fields}
        for v in demande_before.values():
            self.assertNotEqual(v, None)
            self.assertNotEqual(v, "")

        # On va sur la page de la demande comme expert
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse(
                    'dem:request-update',
                    kwargs=dict(self.reverse_base, **{'pk': pk}),
                ),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        # Ferme la boîte de dialogue
        # self.selenium.find_element(by=By.ID, value='main-dialog-ok').click()

        time.sleep(10)

        self.selenium.find_element(by=By.ID, value='id_request_table-montant_unitaire_expert_metier').send_keys('1234')
        # self.selenium.find_element(by=By.ID, value='id_materiel_existant').send_keys('2012/23.334')
        # self.selenium.find_element(by=By.ID, value='id_montant_total_expert_metier').send_keys('123400')
        self.selenium.find_element(by=By.ID, value='id_request_table-commentaire_biomed').send_keys('C\'est une bonne idée')

        # # Enregistre la demande
        # save_button = self.selenium.find_elements(by=By.CSS_SELECTOR, value='#form input[name="submit"]')[0]
        # save_button.click()

        # Submit !
        self.selenium.find_elements(by=By.CSS_SELECTOR, value='[value="record-then-update"]')[0].click()

        # On stocke dans une variable les champs spécifiés de la demande APRES modification
        demande = Demande.records.get(pk=pk)
        demande_after = {fieldname: demande._meta.get_field(fieldname).value_to_string(demande) for fieldname in fields}

        # Enregistrement OK ?
        try:
            help_container = self.selenium.find_elements(by=By.CLASS_NAME, value="dialog-message")
            self.assertIn("enregistré", help_container[0].text)
        except:  # noqa
            self.fail()

        # Champs avant == champs après ?
        self.assertEqual(demande_before, demande_after)

    def test_avis_expert_modif_demande_extra_argumentaire(self):
        "L'ajout d'un avis d'expert ne modifie pas l'argumentation étendue de la demande originale"
        pk = 2
        fields = [
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

        # On stocke dans une variable les champs spécifiés de l'argumentaire AVANT modification
        argumentaire = Demande.records.get(num_dmd=pk)
        argumentaire_before = {
            fieldname: argumentaire._meta.get_field(fieldname).value_to_string(argumentaire) for fieldname in fields
        }
        for v in argumentaire_before.values():
            self.assertNotEqual(v, None)
            self.assertNotEqual(v, "")

        # On va sur la page de la demande comme expert
        self.selenium.get(
            "{}{}".format(
                self.live_server_url,
                reverse(
                    'dem:request-update',
                    kwargs=dict(self.reverse_base, **{'pk': pk}),
                ),
            )
        )

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        self.selenium.find_element(by=By.ID, value='id_request_table-montant_unitaire_expert_metier').send_keys('1234')
        # self.selenium.find_element(by=By.ID, value='id_materiel_existant').send_keys('2012/23.334')
        # self.selenium.find_element(by=By.ID, value='id_montant_total_expert_metier').send_keys('123400')
        self.selenium.find_element(by=By.ID, value='id_request_table-commentaire_biomed').send_keys('C\'est une bonne idée')

        # Enregistre la demande
        # save_button = self.selenium.find_elements(by=By.CSS_SELECTOR, value='#form input[name="submit"]')[0]
        # save_button.click()

        # Submit !
        self.selenium.find_elements(by=By.CSS_SELECTOR, value='[value="record-then-update"]')[0].click()

        # Enregistrement OK ?
        try:
            help_container = self.selenium.find_elements(by=By.CLASS_NAME, value="dialog-message")
            self.assertIn("enregistré", help_container[0].text)
        except:  # noqa
            self.fail()

        # Ferme la boîte de dialogue
        self.selenium.find_element(by=By.ID, value='main-dialog-ok').click()

        # On stocke dans une variable les champs spécifiés de la demande APRES modification
        argumentaires = Demande.records.filter(num_dmd=pk)
        self.assertTrue(argumentaires.exists())
        argumentaire_after = {
            fieldname: argumentaire._meta.get_field(fieldname).value_to_string(argumentaires.get()) for fieldname in fields
        }

        # Champs avant == champs après ?
        self.assertEqual(argumentaire_before, argumentaire_after)


class TestsExpert(TestsBaseTestCase):
    def setUp(self):
        super().setUp()
        if config.settings.BIOM_AID_USE_PREFIX:
            self.live_server_url_wprefix = self.live_server_url + '/dem-chuap'
            self.reverse_base = {'url_prefix': 'dem-chuap'}
        self.login('timettvi')

    def test_menu(self):
        "Vérifie qu'on a bien le menu expertise qui apparaît"

        # On va sur la page d'accueil
        self.selenium.get("{}{}".format(self.live_server_url, reverse('dem:cockpit', kwargs=self.reverse_base)))

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        # Liste des liens vers la page expertise
        print('******', 'a[href="' + reverse('dem:expertise', kwargs=self.reverse_base) + '"]')
        link = self.selenium.find_elements(
            by=By.CSS_SELECTOR,
            value='a[href="' + reverse('dem:expertise', kwargs=self.reverse_base) + '"]',
        )
        self.assertGreaterEqual(len(link), 1)


class TestsArbitre(TestsBaseTestCase):
    def setUp(self):
        super().setUp()
        if config.settings.BIOM_AID_USE_PREFIX:
            self.live_server_url_wprefix = self.live_server_url + '/dem-chuap'
            self.reverse_base = {'url_prefix': 'dem-chuap'}
        self.login('arbitre_biomed')

    def test_menu(self):
        "Vérifie qu'on a bien le menu arbitrage qui apparaît"

        # On va sur la page d'accueil
        self.selenium.get("{}{}".format(self.live_server_url, reverse('dem:cockpit', kwargs=self.reverse_base)))

        # Vérification que la page s'affiche bien
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        # Liste des liens vers la page expertise
        link = self.selenium.find_elements(
            by=By.CSS_SELECTOR,
            value='a[href="'
            + reverse(
                'dem:arbitrage',
                kwargs=dict(self.reverse_base, **{'programme_code': 'BIO-00-PE'}),
            )
            + '"]',
        )
        self.assertGreaterEqual(len(link), 1)
