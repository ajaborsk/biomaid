# Generated by Django 3.2.6 on 2021-08-23 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0041_auto_20210822_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='intitule',
            field=models.CharField(blank=True, help_text="Description de l'alerte", max_length=4096, null=True, verbose_name='Intitulé'),
        ),
    ]
