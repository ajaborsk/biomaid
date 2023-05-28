"""This is a fake Oracle backend, which always claims that Oracle database version is supported (whenever it's true or not)
This restore the buggy but sometime useful pre-4.1 django behaviour
"""

from django.db.backends.oracle import base


class DatabaseWrapper(base.DatabaseWrapper):
    def check_database_version_supported(self):
        return True
