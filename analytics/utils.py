from django.utils.translation import gettext_lazy as _
from django.apps import apps


def set_datasource_in_migration(
    code: str,
    label=None,
    parameters=None,
    auto=None,
    processor=None,
) -> bool:
    datasource_model = apps.get_model('analytics', 'DataSource')

    # return False
    datasource, created = datasource_model.objects.get_or_create(code=code)
    datasource.label = label or ''
    datasource.parameters = parameters or {}
    datasource.auto = auto or []

    if isinstance(processor, str):
        if processor not in apps.get_app_config('analytics').data_processors:
            raise RuntimeError(
                _("Unknown processor name: '{}' not in ('{}')").format(
                    processor, "', '".join(list(apps.get_app_config('analytics').data_processors.keys()))
                )
            )
        else:
            processor_name = processor
    else:
        raise RuntimeError(_("Unable to get data processor {}: Unknow type").format(repr(processor)))
    datasource.processor_name = processor_name

    datasource.save()

    return created
