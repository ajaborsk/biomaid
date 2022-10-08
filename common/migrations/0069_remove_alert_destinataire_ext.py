# Generated by Django 4.0.4 on 2022-05-21 10:02

from django.db import migrations

def destinataire_ext_2_destinataire(apps, schema_editor):
    model = apps.get_model('common', 'Alert')
    records = model.objects.all()
    for record in records:
        if record.destinataire_ext:
            record.destinataire = record.destinataire_ext.user
            record.save(update_fields = ['destinataire'])


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0068_alert_destinataire'),
    ]

    operations = [
        migrations.RunPython(destinataire_ext_2_destinataire),
    ]
