# Generated by Django 3.0.7 on 2021-02-23 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0027_programme_etablissement'),
    ]

    operations = [
        migrations.AddField(
            model_name='fournisseur',
            name='nom',
            field=models.CharField(default=0, max_length=180),
            preserve_default=False,
        ),
    ]
