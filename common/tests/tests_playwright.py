from typing import Callable

import pytest
from playwright.sync_api import Page, expect


# Even with an incorrect url scheme, it should works (lead to a error page, not a 500 server error)
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


# Ensure a non registred user can try (and fail) to connect himself
def test_main_page_fail_connect(live_server, page: Page):
    page.goto(live_server.url)
    expect(page.get_by_role('main')).to_be_visible()

    page.get_by_label("Nom d’utilisateur :").fill('azertyuiop')
    page.locator("input[name=\"password\"]").fill('qsdfghjklm')
    page.get_by_role("button", name="Se connecter").click()

    expect(page.locator('#main-dialog .dialog .dialog-message')).to_contain_text('ne permettent pas de vous connecter')


# Very basic connection test (main page)
@pytest.mark.django_db
def test_example(biomaid_page: Callable) -> None:
    page: Page = biomaid_page('dem:home')
    expect(page.get_by_role('main')).to_be_visible()
    expect(page.locator('#main-dialog .dialog .dialog-message')).not_to_contain_text('ne permettent pas de vous connecter')


@pytest.mark.django_db
@pytest.fixture
def logged(live_server, page: Page, username='deboziel', password='yQ6FfiKypa7h8Hc'):
    page.goto(live_server.url)

    expect(page.get_by_role('main')).to_be_visible()

    page.get_by_label("Nom d’utilisateur :").fill(username)
    page.locator("input[name=\"password\"]").fill(password)
    page.get_by_role("button", name="Se connecter").click()

    expect(page.get_by_role('main')).to_be_visible()

    return page


@pytest.mark.parametrize('username', ['enbaveyv', 'deboziel', 'cekilesy', 'couranth', 'tomiela', 'timettvi'])
def test_login(biomaid_page: Callable, username) -> None:
    page: Page = biomaid_page('dem:home', username=username, password='yQ6FfiKypa7h8Hc')
    expect(page.get_by_role('main')).to_be_visible()
