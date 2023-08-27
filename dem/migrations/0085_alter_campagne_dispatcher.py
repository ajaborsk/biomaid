# Generated by Django 4.2.3 on 2023-08-22 06:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dem', '0084_alter_demande_avis_cadre_sup_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campagne',
            name='dispatcher',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to=settings.AUTH_USER_MODEL,
                verbose_name='Dispatcher',
            ),
        ),
    ]