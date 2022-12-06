from django.utils.translation import gettext as _

from extable.engines import ExtableEngine


class DatabaseEngine(ExtableEngine):
    @staticmethod
    def filename_match(filename: str) -> bool:
        if filename.endswith('__DATABASE__'):
            return True
        return False

    def update(self, msg_callback=None, options={}):
        if msg_callback is not None:
            msg_callback(_("Database engine not yet implemented. Ignoring this extable."))
