import inspect
from types import CodeType

from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analytics'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_processors = {}

    def register_data_processor(self, name: str, f: CodeType) -> bool:
        if name not in self.data_processors:
            self.data_processors[name] = {'function': f, 'parameters': inspect.signature(f).parameters}
            return True
        else:
            return False
