# Generated by Django 3.2.4 on 2021-08-09 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0039_extensionuser_last_seen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='dernier_email',
            field=models.DateTimeField(blank=True, null=True, verbose_name="date d'envoi dernier email"),
        ),
    ]
