from typing import Callable
import re

# import pytest
import time_machine
from playwright.sync_api import Page

from dem.models import Demande


@time_machine.travel("2020-08-15 09:00 +0000")
def test_saisie(biomaid_page: Callable) -> None:
    page: Page = biomaid_page('dem:home', username='couranth', password='yQ6FfiKypa7h8Hc')
    page.get_by_text("Nouvelle demande").click()
    page.get_by_role("link", name="Campagne de test").click()
    page.get_by_label("Unité Fonctionnelle").click()
    page.get_by_label("Unité Fonctionnelle").fill("0003")
    page.get_by_label("Unité Fonctionnelle").press("Tab")
    page.get_by_text("0003 - Orthopédie Est").click()
    page.get_by_label("Matériel demandé").click()
    page.get_by_label("Matériel demandé").fill("Matériel nécessaire")
    page.get_by_label("Quantité").click()
    page.get_by_label("Quantité").fill("6")
    page.get_by_label("Prix unitaire (TTC)").click()
    page.get_by_label("Prix unitaire (TTC)").fill("300")
    page.get_by_role("button", name="Enregistrer et ajouter un autre élément").click()
    page.get_by_role("button", name="C'est noté").click()


def test_full_dispatch_ok(biomaid_page: Callable) -> None:
    # Check the value stored in the database
    dem = Demande.objects.filter(code='DEM-2021-00000').get()
    assert dem.programme is None
    assert dem.domaine is None
    assert dem.expert_metier is None

    # Open main page, logged as a dispatcher
    page: Page = biomaid_page('dem:home', username='tomiela', password='yQ6FfiKypa7h8Hc')

    # Got to the main page of 'dem' portal
    page.goto_name('dem:cockpit', portal='dem')

    # Choose the menu entry
    page.get_by_text("Répartition").click()
    page.get_by_role("link", name="Campagne de test").click()

    # Locate the SmartView table cell with 'expert_metier'
    loc = page.table_locator('repartition_table-smart-view-table', 'code', 'DEM-2021-00000', 'expert_metier')

    # Fill the cell with a value (choosen in the dropdown menu)
    loc.click()
    loc.locator("input[type=\"text\"]").press(" ")
    page.locator(".tabulator-edit-list-item").filter(has_text=re.compile(r"^Jean Bonbeure$")).click()

    # Check if value is displayed
    loc.filter(has_text="bonbeuje").wait_for()
    assert loc.filter(has_text="bonbeuje").count() == 1

    # Locate the SmartView table cell with 'programme'
    loc = page.table_locator('repartition_table-smart-view-table', 'code', 'DEM-2021-00000', 'programme')

    # Fill the cell with a value (choosen in the dropdown menu)
    loc.click()
    loc.locator("input[type=\"text\"]").press(" ")
    page.locator(".tabulator-edit-list-item").filter(has_text=re.compile(r"^Programme courant biomédical$")).click()

    # Check if value is displayed
    loc.filter(has_text="Programme courant biomédical").wait_for()
    assert loc.filter(has_text="Programme courant biomédical").count() == 1

    # Locate the SmartView table cell with 'domaine'
    loc = page.table_locator('repartition_table-smart-view-table', 'code', 'DEM-2021-00000', 'domaine')

    # Fill the cell with a value (choosen in the dropdown menu)
    loc.click()
    loc.locator("input[type=\"text\"]").press(" ")
    page.locator(".tabulator-edit-list-item").filter(has_text=re.compile(r"^324 - Perfusion / Nutrition / Transfusion$")).click()

    # Check if value is displayed
    loc.filter(has_text="324 - Perfusion / Nutrition / Transfusion").wait_for()
    assert loc.filter(has_text="324 - Perfusion / Nutrition / Transfusion").count() == 1

    # Check the values stored in the database
    dem = Demande.objects.filter(code='DEM-2021-00000').get()
    assert dem.programme.code == 'BIO-00-PE'
    assert dem.domaine.code == '324'
    assert dem.expert_metier.username == 'bonbeuje'
