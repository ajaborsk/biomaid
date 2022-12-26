from django.utils.translation import gettext as _
from common.command import BiomAidCommand

from extable.engines import ExtableEngine


class DatabaseEngine(ExtableEngine):
    @staticmethod
    def filename_match(filename: str) -> bool:
        if filename.endswith('__DATABASE__'):
            return True
        return False

    def update(self, log, progress, options={}):
        log(BiomAidCommand.WARNING, _("  Database engine not yet implemented. Ignoring this extable."))
