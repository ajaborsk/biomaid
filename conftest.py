import os
from typing import Any
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


class BiomaidPage:
    def __init__(self, page, base_url, *args, timeout=10000, **kwargs):
        self.page = page
        self.base_url = base_url
        self.portal = 'geqip'
        self.site = 'chuap'
        self.theme = None

        self.page.set_default_timeout(timeout)
        self.page.set_default_navigation_timeout(timeout)

    @property
    def prefix(self):
        return self.portal + '-' + self.site

    def goto_name(self, url_name, portal=None, site=None):
        if portal is not None:
            self.portal = portal
        if site is not None:
            self.site = site
        self.page.goto(self.base_url + reverse(url_name, kwargs={'url_prefix': self.prefix}))

    def table_locator(self, table_id, id_column, id_value, column):
        loc = (
            self.page.locator('#' + table_id)
            .locator('.tabulator-row')
            .filter(
                has=self.page.locator('[tabulator-field="' + id_column + '"]').get_by_text(  # .get_by_role('gridcell')
                    str(id_value), exact=True
                )
            )
            .locator('[tabulator-field="' + column + '"]')
        )
        loc.scroll_into_view_if_needed()
        return loc

    def table_tool_locator(self, table_id, id_column, id_value, iconname):
        loc = (
            self.page.locator('#' + table_id)
            .locator('.tabulator-row')
            .filter(
                has=self.page.locator('[tabulator-field="' + id_column + '"]').get_by_text(  # .get_by_role('gridcell')
                    str(id_value), exact=True
                )
            )
            .locator('i.' + iconname)
        )
        loc.scroll_into_view_if_needed()
        return loc

    def __getattr__(self, __name: str) -> Any:
        return getattr(self.page, __name)


@pytest.fixture(scope='function')
@pytest.mark.django_db
def biomaid_page(live_server, page: Page) -> Page:
    def the_page(url_name, username='couranth', password='yQ6FfiKypa7h8Hc'):
        # goto home page
        biomaid_page = BiomaidPage(page, live_server.url)
        biomaid_page.goto_name('dem:home')
        biomaid_page.get_by_label("Nom d’utilisateur :").fill(username)
        biomaid_page.locator("input[name=\"password\"]").fill(password)
        biomaid_page.get_by_role("button", name="Se connecter").click()
        expect(biomaid_page.locator('#main-dialog .dialog .dialog-message')).not_to_contain_text(
            'ne permettent pas de vous connecter'
        )
        biomaid_page.goto_name(url_name)
        return biomaid_page

    # erase cache
    if 'FileBasedCache' in settings.CACHES['default']['BACKEND']:
        os.system('rm -Rf ' + repr(settings.CACHES['default']['LOCATION']) + '/*')

    return the_page
