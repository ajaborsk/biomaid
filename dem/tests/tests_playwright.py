from typing import Callable
import re

import pytest
import time_machine
from playwright.sync_api import Page, expect

from dem.models import Demande

recorded_dialog_text_re = re.compile(r"Demande (DEM-\d\d\d\d-\d\d\d\d\d) enregistrée avec succès")


def test_new_campaign(biomaid_page: Callable):
    code = 'CPN'
    name = "New Campaign"

    page: Page = biomaid_page('dem:home', username='root', password='introuvable')
    page.get_by_role("listitem").filter(
        has_text="Outils du Manager Gestion des demandes de matériel Demandes Réalisation ACHAts ("
    ).locator("i").click()
    page.get_by_role("link", name="Outils du Manager").click()
    page.get_by_role("link", name="Gestion des calendriers/campagnes").click()
    page.get_by_role("link", name="Ajouter une campagne").click()
    page.get_by_label("Code").click()
    page.get_by_label("Code").fill(code)
    page.get_by_label("Nom").click()
    page.get_by_label("Nom").fill(name)
    page.get_by_label("Description").click()
    page.get_by_label("Description").fill("Description")
    page.get_by_label("Message à l'utilisateur").click()
    page.get_by_label("Message à l'utilisateur").fill("message")
    page.get_by_label("Equipements").check()
    page.get_by_label("Logiciels").check()
    page.get_by_role("combobox", name="Répartisseur").select_option("10")
    page.get_by_label("Date début des demandes").click()
    page.get_by_label("Date début des demandes").fill("01/01/2021")
    page.get_by_label("Date de fin des demandes").click()
    page.get_by_label("Date de fin des demandes").fill("31/12/2023")
    page.get_by_role("button", name="Ajouter et retour à la liste").click()
    page.get_by_role("button", name="C'est noté").click()


@time_machine.travel("2020-08-15 09:00 +0000")
@pytest.mark.parametrize(
    ('user', 'uf_code', 'failure_point'),
    [
        ('couranth', '0003 - ', None),
        ('tomiela', '1001 - ', 'no_campaign'),
        ('deboziel', '0001 - ', None),
        ('deboziel', '0002 - ', None),
        ('deboziel', '0003 - ', None),
        ('enbaveyv', '0001 - ', 'no_uf'),
        ('enbaveyv', '0003 - ', None),
        ('timettvi', '0001 - ', None),
        ('timettvi', '0002 - ', None),
        ('timettvi', '0003 - ', None),
        ('cekilesy', '0001 - ', 'no_uf'),
        ('cekilesy', '0002 - ', 'no_uf'),
        ('cekilesy', '0003 - ', None),
        ('bonbeuje', '0001 - ', None),  # There is no disciplin filtering to be able to create a new request
        ('bonbeuje', '0002 - ', None),  # There is no disciplin filtering to be able to create a new request
        ('bonbeuje', '0003 - ', None),  # There is no disciplin filtering to be able to create a new request
        ('zonloilo', '0003 - ', 'no_campaign'),
        ('igonnepa', '0003 - ', 'no_campaign'),
    ],
)
def test_new_request_minimal(biomaid_page: Callable, user, uf_code, failure_point) -> None:
    "Saisie d'une demande minimale par un cadre, dans une campagne sur un établissement entier"
    # used fields values
    campaign = "Recensement équipements 2021"
    quantity = 6
    requested = "Matériel dont j'ai besoin"

    page: Page = biomaid_page('dem:home', username=user, password='yQ6FfiKypa7h8Hc')
    # ensure we are on the dem portal
    page.locator("li").filter(has_text="Portail BiomAid : Equipements").locator("i").click()
    page.get_by_role("link", name="Portail BiomAid : Equipements").click()

    page.get_by_text("Nouvelle demande").click()
    if failure_point == 'no_campaign':
        expect(page.get_by_role("link", name=campaign)).not_to_be_visible()
        return
    page.get_by_role("link", name=campaign).click()
    page.get_by_label("Unité Fonctionnelle").click()
    if failure_point == 'no_uf':
        expect(page.get_by_role('option').get_by_text(uf_code)).not_to_be_visible()
        return
    page.get_by_role('option').get_by_text(uf_code).click()
    page.get_by_label("Matériel demandé").click()
    page.get_by_label("Matériel demandé").fill(requested)
    page.get_by_label("Quantité").click()
    page.get_by_label("Quantité").fill(str(quantity))
    page.get_by_role("button", name="Enregistrer et ajouter un autre élément").click()
    dialog_text = page.locator('#main-dialog').get_by_text(recorded_dialog_text_re).inner_text()
    page.get_by_role("button", name="C'est noté").click()
    m = recorded_dialog_text_re.search(dialog_text)
    request = Demande.records.get(code=m.group(1))
    assert request.redacteur.username == user
    assert str(request.uf).startswith(uf_code)
    assert request.calendrier.nom == campaign
    assert request.libelle == requested
    assert request.nom_projet == requested
    assert int(request.quantite) == int(quantity)
    assert request.cause == 'AQ'  # default value


@time_machine.travel("2020-09-01 09:00 +0000")
@pytest.mark.parametrize(
    ('user', 'uf_code', 'failure_point'),
    [
        ('couranth', '0003 - ', None),
        ('tomiela', '1001 - ', 'no_campaign'),
        ('deboziel', '0001 - ', None),
        ('deboziel', '0002 - ', None),
        ('deboziel', '0003 - ', None),
        ('enbaveyv', '0001 - ', 'no_uf'),
        ('enbaveyv', '0003 - ', None),
        ('timettvi', '0001 - ', None),
        ('timettvi', '0002 - ', None),
        ('timettvi', '0003 - ', None),
        ('cekilesy', '0001 - ', 'no_uf'),
        ('cekilesy', '0002 - ', 'no_uf'),
        ('cekilesy', '0003 - ', None),
        ('bonbeuje', '0001 - ', None),  # There is no disciplin filtering to be able to create a new request
        ('bonbeuje', '0002 - ', None),  # There is no disciplin filtering to be able to create a new request
        ('bonbeuje', '0003 - ', None),  # There is no disciplin filtering to be able to create a new request
        ('zonloilo', '0003 - ', 'no_campaign'),
        ('igonnepa', '0003 - ', 'no_campaign'),
    ],
)
def test_new_request_full(biomaid_page: Callable, user, uf_code, failure_point) -> None:
    "Saisie d'une demande complète par un utilisateur, dans une campagne sur un établissement entier"
    # used fields values
    campaign = "Recensement équipements 2021"
    quantity = 6
    requested = "Matériel dont j'ai besoin"
    project_name = "Mise à niveau du service"
    unit_price = 314159
    # description = "Voilà exactement le matériel dont j'ai besoin"

    page: Page = biomaid_page('dem:home', username=user, password='yQ6FfiKypa7h8Hc')
    # ensure we are on the dem portal
    page.locator("li").filter(has_text="Portail BiomAid : Equipements").locator("i").click()
    page.get_by_role("link", name="Portail BiomAid : Equipements").click()

    page.get_by_text("Nouvelle demande").click()
    if failure_point == 'no_campaign':
        expect(page.get_by_role("link", name=campaign)).not_to_be_visible()
        return
    page.get_by_role("link", name=campaign).click()
    page.get_by_label("Unité Fonctionnelle").click()
    if failure_point == 'no_uf':
        expect(page.get_by_role('option').get_by_text(uf_code)).not_to_be_visible()
        return
    page.get_by_role('option').get_by_text(uf_code).click()
    page.get_by_label("Matériel demandé").click()
    page.get_by_label("Matériel demandé").fill(requested)
    page.get_by_label("Nom du projet").click()
    page.get_by_label("Nom du projet").fill(project_name)
    page.get_by_label("Quantité").click()
    page.get_by_label("Quantité").fill(str(quantity))
    page.get_by_label("Prix unitaire").click()
    page.get_by_label("Prix unitaire").fill(str(unit_price))
    page.get_by_role("button", name="Enregistrer et ajouter un autre élément").click()
    dialog_text = page.locator('#main-dialog').get_by_text(recorded_dialog_text_re).inner_text()
    page.get_by_role("button", name="C'est noté").click()
    m = recorded_dialog_text_re.search(dialog_text)
    request = Demande.records.get(code=m.group(1))
    assert request.redacteur.username == user
    assert str(request.uf).startswith(uf_code)
    assert request.calendrier.nom == campaign
    assert request.libelle == requested
    assert request.nom_projet == project_name
    assert int(request.quantite) == int(quantity)
    assert int(request.prix_unitaire) == int(unit_price)
    assert request.cause == 'AQ'


@time_machine.travel("2020-06-01 09:00 +0000")
@pytest.mark.parametrize(
    ('user', 'uf_code', 'failure_point'),
    [
        ('couranth', '0003 - ', 'no_campaign'),
        ('tomiela', '1001 - ', 'no_campaign'),
        ('deboziel', '0001 - ', 'no_campaign'),
        ('deboziel', '0002 - ', 'no_campaign'),
        ('deboziel', '0003 - ', 'no_campaign'),
        ('enbaveyv', '0001 - ', 'no_campaign'),
        ('enbaveyv', '0003 - ', 'no_campaign'),
        ('timettvi', '0001 - ', 'no_campaign'),
        ('timettvi', '0002 - ', 'no_campaign'),
        ('timettvi', '0003 - ', 'no_campaign'),
        ('cekilesy', '0001 - ', 'no_campaign'),
        ('cekilesy', '0002 - ', 'no_campaign'),
        ('cekilesy', '0003 - ', 'no_campaign'),
        ('bonbeuje', '0001 - ', 'no_campaign'),
        ('bonbeuje', '0002 - ', 'no_campaign'),
        ('bonbeuje', '0003 - ', 'no_campaign'),
        ('zonloilo', '0003 - ', 'no_campaign'),
        ('igonnepa', '0003 - ', 'no_campaign'),
    ],
)
def test_new_request_minimal_before(biomaid_page: Callable, user, uf_code, failure_point) -> None:
    "Saisie d'une demande minimale par un cadre, dans une campagne sur un établissement entier (test avant l'ouverture de la campagne)"
    campaign = "Recensement équipements 2021"
    page: Page = biomaid_page('dem:home', username=user, password='yQ6FfiKypa7h8Hc')
    # ensure we are on the dem portal
    page.locator("li").filter(has_text="Portail BiomAid : Equipements").locator("i").click()
    page.get_by_role("link", name="Portail BiomAid : Equipements").click()

    page.get_by_text("Nouvelle demande").click()
    if failure_point == 'no_campaign':
        expect(page.get_by_role("link", name=campaign)).not_to_be_visible()
        return
    assert False  # Should never get there !


@time_machine.travel("2020-12-01 09:00 +0000")
@pytest.mark.parametrize(
    ('user', 'uf_code', 'failure_point'),
    [
        ('couranth', '0003 - ', 'no_campaign'),
        ('tomiela', '1001 - ', 'no_campaign'),
        ('deboziel', '0001 - ', 'no_campaign'),
        ('deboziel', '0002 - ', 'no_campaign'),
        ('deboziel', '0003 - ', 'no_campaign'),
        ('enbaveyv', '0001 - ', 'no_campaign'),
        ('enbaveyv', '0003 - ', 'no_campaign'),
        ('timettvi', '0001 - ', 'no_campaign'),
        ('timettvi', '0002 - ', 'no_campaign'),
        ('timettvi', '0003 - ', 'no_campaign'),
        ('cekilesy', '0001 - ', 'no_campaign'),
        ('cekilesy', '0002 - ', 'no_campaign'),
        ('cekilesy', '0003 - ', 'no_campaign'),
        ('bonbeuje', '0001 - ', 'no_campaign'),
        ('bonbeuje', '0002 - ', 'no_campaign'),
        ('bonbeuje', '0003 - ', 'no_campaign'),
        ('zonloilo', '0003 - ', 'no_campaign'),
        ('igonnepa', '0003 - ', 'no_campaign'),
    ],
)
def test_new_request_minimal_after(biomaid_page: Callable, user, uf_code, failure_point) -> None:
    "Saisie d'une demande minimale par un cadre, dans une campagne sur un établissement entier (test après la fermeture de la campagne)"
    campaign = "Recensement équipements 2021"
    page: Page = biomaid_page('dem:home', username=user, password='yQ6FfiKypa7h8Hc')
    # ensure we are on the dem portal
    page.locator("li").filter(has_text="Portail BiomAid : Equipements").locator("i").click()
    page.get_by_role("link", name="Portail BiomAid : Equipements").click()

    page.get_by_text("Nouvelle demande").click()
    if failure_point == 'no_campaign':
        expect(page.get_by_role("link", name=campaign)).not_to_be_visible()
        return
    assert False  # Should never get there !


def test_modify_request_in_table(biomaid_page: Callable) -> None:
    # Open main page, logged as a requester
    page: Page = biomaid_page('dem:home', username='couranth', password='yQ6FfiKypa7h8Hc')

    # Go to the main page of 'dem' portal
    page.goto_name('dem:home', portal='geqip')

    # Go to current requests page
    page.get_by_role("link", name="Demandes à approuver").click()

    # Locate the SmartView table cell with 'cause'
    loc = page.table_locator('demandes_a_approuver_table-smart-view-table', 'code', 'DEM-2021-00000', 'cause')
    loc.click()

    # unfinished test
    assert False, "Unfinished test"


def test_modify_request_in_form(biomaid_page: Callable) -> None:
    # Open main page, logged as a requester
    page: Page = biomaid_page('dem:home', username='couranth', password='yQ6FfiKypa7h8Hc')

    # Go to the main page of 'dem' portal
    page.goto_name('dem:home', portal='geqip')

    # Go to current requests page
    page.get_by_role("link", name="Demandes à approuver").click()

    # Locate the SmartView table cell with 'cause'
    loc = page.table_tool_locator('demandes_a_approuver_table-smart-view-table', 'code', 'DEM-2021-00000', 'fa-edit')
    loc.click()

    # unfinished test
    assert False, "Unfinished test"


def test_reroute_request_to_other_campaign(biomaid_page: Callable) -> None:
    # unfinished test
    assert False, "Unfinished test"


def test_reroute_request_to_virtual_campaign(biomaid_page: Callable) -> None:
    # unfinished test
    assert False, "Unfinished test"


def test_full_dispatch_in_table_ok(biomaid_page: Callable) -> None:
    # Check the value stored in the database
    dem = Demande.records.filter(code='DEM-2021-00000').get()
    assert dem.programme is None
    assert dem.domaine is None
    assert dem.expert_metier is None

    # Open main page, logged as a dispatcher
    page: Page = biomaid_page('dem:home', username='tomiela', password='yQ6FfiKypa7h8Hc')

    # Go to the main page of 'dem' portal
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
    dem = Demande.records.filter(code='DEM-2021-00000').get()
    assert dem.programme.code == 'BIO-00-PE'
    assert dem.domaine.code == '324'
    assert dem.expert_metier.username == 'bonbeuje'


def test_dispatch_in_table_expert_only(biomaid_page: Callable) -> None:
    # Check the value stored in the database
    dem = Demande.records.filter(code='DEM-2021-00000').get()
    assert dem.programme is None
    assert dem.domaine is None
    assert dem.expert_metier is None

    # Open main page, logged as a dispatcher
    page: Page = biomaid_page('dem:home', username='tomiela', password='yQ6FfiKypa7h8Hc')

    # Go to the main page of 'dem' portal
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
    dem = Demande.records.filter(code='DEM-2021-00000').get()
    assert dem.programme.code == 'BIO-00-PE'
    assert dem.domaine.code == '324'
    assert dem.expert_metier.username == 'bonbeuje'

    # unfinished test
    assert False, "Unfinished test"


def test_dispatch_in_table_program_only(biomaid_page: Callable) -> None:
    # Check the value stored in the database
    dem = Demande.records.filter(code='DEM-2021-00000').get()
    assert dem.programme is None
    assert dem.domaine is None
    assert dem.expert_metier is None

    # Open main page, logged as a dispatcher
    page: Page = biomaid_page('dem:home', username='tomiela', password='yQ6FfiKypa7h8Hc')

    # Go to the main page of 'dem' portal
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
    dem = Demande.records.filter(code='DEM-2021-00000').get()
    assert dem.programme.code == 'BIO-00-PE'
    assert dem.domaine.code == '324'
    assert dem.expert_metier.username == 'bonbeuje'

    # unfinished test
    assert False, "Unfinished test"
