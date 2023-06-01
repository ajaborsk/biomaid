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

import logging


from settings import DEBUG_TOOLBAR, MIDDLEWARE, INSTALLED_APPS

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(name)s %(levelname)s %(message)s', datefmt='%Y-%m-%dT%H:%M:%S')
logging.getLogger(__name__).info("MKTEST.")

DEFAULT_DOMAIN = 'http://localhost:8000'

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

DEBUG = False
TEMPLATE_DEBUG = DEBUG
SMARTVIEW_DEBUG = DEBUG

AUTHENTICATION_BACKENDS = ('common.auth_backends.MyAuthBackend',)

# Get some print()...
OVEROLY_DEBUG = DEBUG

# If True, anything that is not explicitly authorized is denied
# If False (default), any object with no explicit authorization information isn't checked
OVEROLY_STRICT = True

# For class based views, which attribute is used for permissions
# default is 'overoly_permissions'
OVEROLY_VIEW_PERMISSIONS_ATTRIBUTE_NAME = 'permissions'

if DEBUG_TOOLBAR:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + MIDDLEWARE
    INTERNAL_IPS = [
        # ...
        '127.0.0.1',
        # ...
    ]

INSTALLED_APPS += [
    #    'mptt',
    # 'dra94',
]

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': 'db.sqlite3',
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mktest_db',
        'USER': 'mktest_user',
        'PASSWORD': 'mktest_pwd',  # Utilisé seulement pour les tests en local
        'HOST': 'localhost',
        'PORT': '',
    },
}

# local email tests on port 8025 (using aiosmtpd python module)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 8025

DRA94_CFG = {
    'data_path': '../dem--dra94/',
}

MAGH2_CFG = {
    'data_path': '../dem--magh2/',
}

MEDIA_ROOT = '../dem-media'
