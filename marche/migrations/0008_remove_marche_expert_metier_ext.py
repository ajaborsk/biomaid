#  Copyright (c)

# Generated by Django 4.0.4 on 2022-05-20 19:51

from django.db import migrations

def expert_ext_2_expert(apps, schema_editor):
    model = apps.get_model('marche', 'Marche')
    records = model.objects.all()
    for record in records:
        if record.expert_metier_ext:
            record.expert_metier = record.expert_metier_ext.user
            record.save(update_fields = ['expert_metier'])


class Migration(migrations.Migration):

    dependencies = [
        ('marche', '0007_marche_expert_metier_alter_marche_expert_metier_ext'),
    ]

    operations = [
        migrations.RunPython(expert_ext_2_expert),
    ]
