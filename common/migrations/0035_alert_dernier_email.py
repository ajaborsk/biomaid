# Generated by Django 3.1.4 on 2021-05-02 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0034_extensionuser_preferences'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='dernier_email',
            field=models.DateTimeField(blank=True, null=True, verbose_name="date d'envoi dernier email'"),
        ),
    ]
