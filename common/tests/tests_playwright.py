from typing import Callable

import pytest
from playwright.sync_api import Page, expect

# from dem.models import Demande


@pytest.mark.parametrize(
    'path',
    [
        '/',
        '/default/',
        '/portal-config/',
        '/portal-config-theme/',
        '/geqip-chuap/',
        '/geqip-badconfig/',
        '/geqip/common/user_alerts/',
    ],
)
def test_main_page_path(live_server, page: Page, path):
    page.goto(live_server.url + path)
    expect(page.get_by_role('main')).to_be_visible()


def test_main_page_fail_connect(live_server, page: Page):
    page.goto(live_server.url)
    expect(page.get_by_role('main')).to_be_visible()

    page.get_by_label("Nom d’utilisateur :").fill('azertyuiop')
    page.locator("input[name=\"password\"]").fill('qsdfghjklm')
    page.get_by_role("button", name="Se connecter").click()

    expect(page.locator('#main-dialog .dialog .dialog-message')).to_contain_text('ne permettent pas de vous connecter')


@pytest.mark.django_db
def test_example(biomaid_page: Callable) -> None:
    page: Page = biomaid_page('dem:home')
    expect(page.get_by_role('main')).to_be_visible()

    expect(page.locator('#main-dialog .dialog .dialog-message')).not_to_contain_text('ne permettent pas de vous connecter')
