import logging

from django.core.management.base import BaseCommand


class BiomAidCommand(BaseCommand):
    DEBUG = logging.DEBUG
    FINE = (logging.DEBUG + logging.INFO) // 2
    INFO = logging.INFO
    WARN = logging.WARN
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    FATAL = logging.FATAL

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logging.getLogger(self.__module__)

    def log(self, level, message):
        self.logger.log(level, message)
