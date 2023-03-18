from django.contrib import admin

# Register your models here.
from django.contrib.admin import ModelAdmin

from analytics.models import Data, DbDataSource


class DataSourceAdmin(ModelAdmin):
    list_display = (
        'code',
        'label',
        'description',
        'processor_name',
        'cloture',
    )
    list_filter = (
        'processor_name',
        'cloture',
    )
    search_fields = (
        'code',
        'label',
        'description',
    )


class DataAdmin(ModelAdmin):
    list_display = (
        'source',
        'parameters',
        'timestamp',
        'data',
    )
    list_filter = ('source',)


admin.site.register(DbDataSource, DataSourceAdmin)
admin.site.register(Data, DataAdmin)
