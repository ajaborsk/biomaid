# Generated by Django 4.0 on 2022-11-20 17:44

from django.db import migrations
from django.utils.translation import gettext_lazy as _

from analytics.utils import set_datasource_in_migration

def add_datasources(apps, schema_editor):
#     set_datasource_in_migration('drachar.previsionnel.count', {}, processor=lambda: None)
    set_datasource_in_migration('drachar.previsionnel-par-expert', {}, processor='previsionnel_par_expert')
    set_datasource_in_migration('drachar.montant-previsionnel-par-expert', {}, processor='montant_previsionnel_par_expert')


class Migration(migrations.Migration):

    dependencies = [
        ('drachar', '0028_remove_documentdracharlink_document_and_more'),
    ]

    operations = [
        migrations.RunPython(add_datasources),
    ]