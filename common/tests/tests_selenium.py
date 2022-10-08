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
import os
import time
from html.parser import HTMLParser
from unittest.util import strclass

import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from parameterized import parameterized

from common import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ["PATH"] += os.pathsep + os.path.join(BASE_DIR, '/gecko')
pytestmark = pytest.mark.django_db


class GetLinksHtmlParser(HTMLParser):
    def __init__(self, prefix='/'):
        super().__init__()
        self.prefix = prefix
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag.upper() == 'A':
            url = dict(attrs).get('href')
            if isinstance(url, str) and url.startswith(self.prefix):
                self.links.append(url)

    def get_links(self):
        return self.links


@pytest.mark.django_db
class EmptyBaseTests(StaticLiveServerTestCase):
    pytestmark = pytest.mark.django_db

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def __str__(self):
        return "%s.%s" % (strclass(self.__class__), self._testMethodName)

    def setUp(self) -> None:
        if config.settings.BIOM_AID_USE_PREFIX:
            self.live_server_url_wprefix = self.live_server_url + '/geqip-chuap'
            self.reverse_base = {'url_prefix': 'geqip-chuap'}

    @parameterized.expand(
        [
            ('/common/accueil',),
            ('/login',),
            ('/signup',),
        ]
    )
    def test_pages_without_login(self, url):
        """Pages publiques"""
        self.selenium.get("{}{}".format(self.live_server_url_wprefix, url))
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)

        parser = GetLinksHtmlParser()
        parser.feed(self.selenium.page_source)
        for url in parser.get_links():
            self.selenium.get("{}{}".format(self.live_server_url, url))
            self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)


class TestsBaseTestCase(StaticLiveServerTestCase):
    fixtures = ['fixtures/tests_db']
    # Ella de Bozieux, deboziel, yQ6FfiKypa7h8Hc,
    # Sylvie Cekilépamor, cekilesy, yQ6FfiKypa7h8Hc,
    # Théo Courant, couranth, yQ6FfiKypa7h8Hc
    # Yvon Enbaver, enbaveyv, yQ6FfiKypa7h8Hc,
    # Lana Tomie, tomiela, yQ6FfiKypa7h8Hc,

    def __str__(self):
        return "%s.%s" % (strclass(self.__class__), self._testMethodName)

    def check_links(self):
        parser = GetLinksHtmlParser()
        parser.feed(self.selenium.page_source)
        for url in parser.get_links():
            if '/logout/' not in url:
                self.selenium.get("{}{}".format(self.live_server_url, url))
                self.assertTrue(
                    len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')) == 1
                    or len(self.selenium.find_elements(by=By.ID, value='branding')) == 1,
                )

    def setUp(self) -> None:
        if config.settings.BIOM_AID_USE_PREFIX:
            self.live_server_url_wprefix = self.live_server_url + '/geqip-chuap'
            self.reverse_base = {'url_prefix': 'geqip-chuap'}

    def login(self, username="deboziel", password="yQ6FfiKypa7h8Hc"):
        self.selenium.get("{}/login".format(self.live_server_url_wprefix))
        self.selenium.find_element(by=By.ID, value='username').send_keys(username)
        self.selenium.find_element(by=By.ID, value='password').send_keys(password)
        buttons = self.selenium.find_elements(by=By.CSS_SELECTOR, value='.login3 button')
        buttons[0].click()

    def get_tabulator_cell(self, table_id, id_field_name, row_id, field_name):
        # Attendre qu'il y ait au moins une ligne dans le tableau (chargement des données par AJAX/JSON...)
        WebDriverWait(self.selenium, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//*[@id='{}']/div[2]/div".format(table_id)))
        )

        rows = self.selenium.find_elements(by=By.CSS_SELECTOR, value='#{} .tabulator-row'.format(table_id))

        for row in rows:
            id_cell = row.find_elements(
                by=By.CSS_SELECTOR,
                value='.tabulator-cell[tabulator-field="{}"]'.format(id_field_name),
            )[0]
            if id_cell.text == row_id:
                element = row.find_elements(
                    by=By.CSS_SELECTOR,
                    value='.tabulator-cell[tabulator-field="{}"]'.format(field_name),
                )[0]
                self.selenium.execute_script(
                    'arguments[0].scrollIntoView({behavior: "smooth", block: "center", inline: "center"})', element
                )
                time.sleep(0.1)
                return element
        return None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(1)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()


class TestsBaseTests(TestsBaseTestCase):
    @parameterized.expand(
        [
            ("Normal", "Jean", "Valjean"),
            ("Accents", "André", "Durand"),
            ("Tirets", "Jean-Luc", "Picard"),
            ("Espaces", "Jean-Luc", "de la Porte"),
        ]
    )
    def test_signup(self, name, first_name, last_name):
        """Inscription sur le site possible"""
        self.selenium.get("{}/signup".format(self.live_server_url_wprefix))
        self.selenium.find_element(by=By.ID, value='main-dialog-ok').click()
        self.selenium.find_element(by=By.ID, value='id_first_name').send_keys(first_name)
        self.selenium.find_element(by=By.ID, value='id_last_name').send_keys(last_name)
        self.selenium.find_element(by=By.ID, value='id_password1').send_keys("Azerty123$%")
        self.selenium.find_element(by=By.ID, value='id_password2').send_keys("Azerty123$%")
        self.selenium.find_element(by=By.NAME, value='submit').click()
        h2 = self.selenium.find_elements(by=By.CSS_SELECTOR, value='.active-tab-content h2')
        self.assertEqual(len(h2), 1)
        self.assertIn("Succès", h2[0].text)
        self.check_links()

    def login(self, username="deboziel", password="yQ6FfiKypa7h8Hc"):
        self.selenium.get("{}/login".format(self.live_server_url_wprefix))
        self.selenium.find_element(by=By.ID, value='username').send_keys(username)
        self.selenium.find_element(by=By.ID, value='password').send_keys(password)
        buttons = self.selenium.find_elements(by=By.CSS_SELECTOR, value='.login3 button')
        buttons[0].click()

    @parameterized.expand(
        [
            ("Super Utilisateur", "root", "introuvable"),
            ("Yvon Enbaver", "enbaveyv", "yQ6FfiKypa7h8Hc"),
            ("Ella de Bozieux", "deboziel", "yQ6FfiKypa7h8Hc"),
            ("Sylvie Cekilépamor", "cekilesy", "yQ6FfiKypa7h8Hc"),
            ("Théo Courant", "couranth", "yQ6FfiKypa7h8Hc"),
            ("Lana Tomie", "tomiela", "yQ6FfiKypa7h8Hc"),
            ("Vincent Timettre", "timettvi", "yQ6FfiKypa7h8Hc"),
            ("Harry Staukrate", "arbitre_biomed", "yQ6FfiKypa7h8Hc"),
        ]
    )
    def test_login(self, name, username, password):
        """Connexion sur le site possible"""
        self.login(username, password)
        title = self.selenium.find_elements(by=By.CSS_SELECTOR, value='.main-tile-title')
        self.assertGreater(len(title), 1)
        self.assertIn("BIENVENUE", title[0].text)
        self.check_links()

    @parameterized.expand(
        [
            ('/common/account',),
            ('/common/profile',),
            ('/common/preferences',),
        ]
    )
    def test_pages_with_login(self, url):
        """Pages nécessitant d'être connecté"""
        self.login()
        self.selenium.get("{}{}".format(self.live_server_url_wprefix, url))
        self.assertEqual(len(self.selenium.find_elements(by=By.CLASS_NAME, value='topbar2')), 1)
        self.check_links()
