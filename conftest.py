from django.urls import reverse
from django.core.management import call_command
import settings

import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope='session')
def django_db_modify_db_settings(django_db_modify_db_settings):
    if 'gmao' in settings.DATABASES:
        del settings.DATABASES['gmao']


# 'session' scope works well for selenium tests
# 'function' scope works well for playwright tests
# 'class' scope seems to work with both :-)
@pytest.fixture(scope='class')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', 'tests_db.json')


@pytest.fixture(scope='function')
@pytest.mark.django_db
def biomaid_page(live_server, page: Page) -> Page:
    def the_page(url_name, prefix='geqip-chuap', username='couranth', password='yQ6FfiKypa7h8Hc'):
        # goto home page
        page.goto(live_server.url + '/' + prefix + '/dem/')
        page.get_by_label("Nom d’utilisateur :").fill(username)
        page.locator("input[name=\"password\"]").fill(password)
        page.get_by_role("button", name="Se connecter").click()
        expect(page.locator('#main-dialog .dialog .dialog-message')).not_to_contain_text('ne permettent pas de vous connecter')
        page.goto(live_server.url + reverse(url_name, kwargs={'url_prefix': prefix}))
        return page

    return the_page
