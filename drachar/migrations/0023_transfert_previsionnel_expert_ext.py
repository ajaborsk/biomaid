#  Copyright (c)

# Generated by Django 4.0.4 on 2022-05-21 13:40

from django.db import migrations

def expert_ext_2_expert(apps, schema_editor):
    model = apps.get_model('drachar', 'Previsionnel')
    records = model.objects.all()
    for record in records:
        if record.expert_ext:
            record.expert = record.expert_ext.user
            record.save(update_fields = ['expert'])


class Migration(migrations.Migration):

    dependencies = [
        ('drachar', '0022_previsionnel_expert'),
    ]

    operations = [
        migrations.RunPython(expert_ext_2_expert),
        # migrations.RemoveField(
        #     model_name='previsionnel',
        #     name='expert_ext',
        # ),
    ]
