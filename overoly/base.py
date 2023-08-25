from django.db.models import Model
from django.db.models.base import ModelBase


class OverolyModelMetaclass(ModelBase):
    def __new__(cls, name, attrs, **kwargs):
        cl = super().__new__(cls, name, attrs, **kwargs)
        print(f"Overoly class {name=}")
        return cl


class OverolyModel(Model, metaclass=OverolyModelMetaclass):
    class Meta:
        abstract = True
