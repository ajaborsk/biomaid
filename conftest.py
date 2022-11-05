from django.urls import reverse
from django.core.management import call_command
import settings

import pytest
from playwright.sync_api import Page


@pytest.fixture(scope='session')
def django_db_modify_db_settings(django_db_modify_db_settings):
    if 'gmao' in settings.DATABASES:
        del settings.DATABASES['gmao']


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'tests_db.json')


@pytest.fixture
@pytest.mark.django_db
def biomaid_page(live_server, page: Page) -> Page:
    page.goto(live_server.url)
    page.get_by_label("Nom d’utilisateur :").fill('deboziel')
    page.locator("input[name=\"password\"]").fill('yQ6FfiKypa7h8Hc')
    page.get_by_role("button", name="Se connecter").click()

    def the_page(url_name):
        page.goto(live_server.url + reverse(url_name, kwargs={'url_prefix': 'cgf-portal'}))
        return page

    return the_page
