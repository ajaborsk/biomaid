# Generated by Django 3.0.5 on 2020-08-21 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0009_auto_20200821_1351'),
    ]

    operations = [
        migrations.AddField(
            model_name='arbitrage',
            name='commentaire',
            field=models.CharField(blank=True, default=None, max_length=160, null=True),
        ),
    ]
