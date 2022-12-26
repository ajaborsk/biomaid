from functools import partial
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

    def get_loggers(self, **options):
        if self._called_from_command_line:

            def console_logger(threshold, level, message):
                if level >= threshold:
                    if level >= self.ERROR:
                        style = self.style.ERROR
                    elif level >= self.WARN:
                        style = self.style.WARNING
                    elif level >= self.INFO:
                        style = self.style.SUCCESS
                    else:
                        style = self.style.MIGRATE_LABEL
                    self.stdout.write(style(message))

            def console_progress(count, total=100):
                self.stdout.write(f"  {count=}/{total=}", ending='\r')

            return partial(console_logger, {0: self.ERROR, 1: self.INFO, 2: self.FINE, 3: self.DEBUG}[options['verbosity']]), (
                console_progress if options['verbosity'] >= 1 else lambda *a: None
            )
        else:
            logger = logging.getLogger(self.__module__)

            def main_logger(level, message):
                logger.log(level, message)

            return main_logger, lambda *a: None
