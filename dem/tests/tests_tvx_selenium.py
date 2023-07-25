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
import time
import urllib.parse

import time_machine
from parameterized import parameterized
from django.urls import reverse
from django.utils.translation import gettext as _

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from common import config
from common.tests.tests_selenium import TestsBaseTestCase
from dem.models import Campagne


class TestsTvxBaseTests(TestsBaseTestCase):
    def setUp(self) -> None:
        if config.settings.BIOM_AID_USE_PREFIX:
            self.live_server_url_wprefix = self.live_server_url + '/kos-chuaptvx'
            self.reverse_base = {'url_prefix': 'kos-chuaptvx'}


class TestsTvxBaseTestsConcrete(TestsTvxBaseTests):
    @parameterized.expand(
        [
            ('dem:tvx-home',),
            ('dem:tvx-demande-create', {'campagne': 'TVXCT'}),
            ('dem:tvx-demande',),
        ]
    )
    def test_acces_pages_with_login_csp(self, url_name, url_params={}):
        """Pages nécessitant d'être connecté"""
        url = (
            reverse(url_name, kwargs=self.reverse_base)
            + '?'
            + urllib.parse.urlencode({'choices': json.dumps({'calendrier': [Campagne.objects.get(code='TVXCT').pk]})})
        )
        # Login comme cadre de pôle
        self.login('enbaveyv')
        self.selenium.get("{}{}".format(self.live_server_url, url))
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        self.check_links()

    @parameterized.expand(
        [
            ('dem:tvx-home',),
            ('dem:tvx-demande-create', {'campagne': 'TVXCT'}),
            ('dem:tvx-demande',),
        ]
    )
    def test_acces_pages_with_login_chp(self, url_name, url_kwargs={}):
        """Pages nécessitant d'être connecté"""
        url = (
            reverse(url_name, kwargs=self.reverse_base)
            + '?'
            + urllib.parse.urlencode({'choices': json.dumps({'calendrier': [Campagne.objects.get(code='TVXCT').pk]})})
        )
        # Login comme cadre de pôle
        self.login('cekilesy')
        self.selenium.get("{}{}".format(self.live_server_url, url))
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        self.check_links()

    @time_machine.travel("2020-08-02 09:00 +0000")
    def test_saisie_demande_chp(self):
        url = (
            reverse(
                'dem:tvx-demande-create',
                kwargs=self.reverse_base,
            )
            + '?'
            + urllib.parse.urlencode({'choices': json.dumps({'calendrier': [Campagne.objects.get(code='TVXCT').pk]})})
        )

        self.login('cekilesy')
        self.selenium.get("{}{}".format(self.live_server_url, url))
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        # Le bâtiment
        self.selenium.find_element(by=By.ID, value='id_tvx_demande_table-tvx_batiment').find_elements(
            by=By.CSS_SELECTOR, value='[value="CBH"]'
        )[0].click()

        # L'étage (no longer needed)
        # self.selenium.find_element(by=By.ID, value='id_tvx_demande_table-tvx_etage').find_elements(
        #     by=By.CSS_SELECTOR, value='[value="RDC"]'
        # )[0].click()

        # Saisie de l'UF
        self.selenium.find_element(by=By.ID, value='id_tvx_demande_table-uf-flexdatalist').send_keys('0003')
        time.sleep(0.5)
        self.selenium.find_element(by=By.ID, value='id_tvx_demande_table-uf-flexdatalist').send_keys(Keys.DOWN, Keys.ENTER)

        # Travaux à faire
        self.selenium.find_element(by=By.ID, value='id_tvx_demande_table-libelle').send_keys("Tout un tas de murs à repeindre")

        # La priorité
        self.selenium.find_element(by=By.ID, value='id_tvx_demande_table-tvx_priorite').find_elements(
            by=By.CSS_SELECTOR, value='[value="2"]'
        )[0].click()

        # Submit !
        self.selenium.find_elements(by=By.CSS_SELECTOR, value='[value="record"]')[0].click()

        # Click ok sur la boîte de dialogue
        self.selenium.find_element(by=By.ID, value='main-dialog-ok').click()

        # Page OK (pas d'erreur 500)
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

    @time_machine.travel("2020-08-02 09:00 +0000")
    def test_saisie_demande_incomplete_chp(self):
        url = (
            reverse(
                'dem:tvx-demande-create',
                kwargs=self.reverse_base,
            )
            + '?'
            + urllib.parse.urlencode({'choices': json.dumps({'calendrier': [Campagne.objects.get(code='TVXCT').pk]})})
        )
        self.login('cekilesy')
        self.selenium.get("{}{}".format(self.live_server_url, url))
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        # Le bâtiment
        self.selenium.find_element(by=By.ID, value='id_tvx_demande_table-tvx_batiment').find_elements(
            by=By.CSS_SELECTOR, value='[value="CBH"]'
        )[0].click()

        # L'étage (no longer needed)
        # self.selenium.find_element(by=By.ID, value='id_tvx_demande_table-tvx_etage').find_elements(
        #     by=By.CSS_SELECTOR, value='[value="RDC"]'
        # )[0].click()

        # Saisie de l'UF
        self.selenium.find_element(by=By.ID, value="id_tvx_demande_table-uf-flexdatalist").clear()
        self.selenium.find_element(by=By.ID, value='id_tvx_demande_table-uf-flexdatalist').send_keys('0003')
        time.sleep(0.5)
        self.selenium.find_element(by=By.ID, value='id_tvx_demande_table-uf-flexdatalist').send_keys(Keys.DOWN, Keys.ENTER)

        # Travaux à faire
        self.selenium.find_element(by=By.ID, value='id_tvx_demande_table-libelle').send_keys("Tout un tas de murs à repeindre")

        # La priorité
        # self.selenium.find_element(by=By.ID, value='id_tvx_demande_table-tvx_priorite')
        #   .find_elements(by=By.CSS_SELECTOR, value='[value="2"]')[0].click()

        # Submit !
        self.selenium.find_elements(by=By.CSS_SELECTOR, value='[value="record"]')[0].click()

        # Click ok sur la boîte de dialogue
        text = self.selenium.find_element(by=By.CSS_SELECTOR, value='.dialog-message').text

        self.assertNotIn('enregistré', text, _("Enregistré malgré tout"))
