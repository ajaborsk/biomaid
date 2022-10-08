# Generated by Django 3.2.4 on 2021-08-09 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0040_alter_alert_dernier_email'),
        ('geprete', '0003_auto_20210809_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gessaye',
            name='ingenieur_responsable',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.extensionuser'),
        ),
        migrations.AlterField(
            model_name='gessaye',
            name='unite_fonctionnelle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.uf'),
        ),
        migrations.DeleteModel(
            name='ExtensionUser',
        ),
    ]
