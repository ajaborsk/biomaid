#  Copyright (c) 2020 Brice Nord, Romuald Kliglich, Alexandre Jaborska, Philomène Mazand.
#  This file is part of the BiomAid distribution.
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.
import pytest


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
def test_main_page_path(live_server, py, path):
    py.visit(live_server.url + path)
    py.get('main')


def test_main_page_fail_connect(live_server, py, test_results_dir):
    py.visit(live_server.url)
    py.get('main')
    py.get('#id_username').type('azertyuiop')
    py.get('#id_password').type('qsdfghjklm')
    py.get('#form-signin button[name=submit]').click()
    # py.get('#main-dialog .dialog .dialog-message').screenshot(os.path.join(test_results_dir, 'dialog.png'))
    assert 'ne permettent pas de vous connecter' in py.get('#main-dialog .dialog .dialog-message').text()


@pytest.mark.django_db
def test_main_page_success_connect(live_server, py):
    py.visit(live_server.url)
    py.get('main')
    py.get('#id_username').type('deboziel')
    py.get('#id_password').type('yQ6FfiKypa7h8Hc')
    py.get('#form-signin button[name=submit]').click()
    assert 'ne permettent pas de vous connecter' not in py.get('#main-dialog .dialog .dialog-message').text()
