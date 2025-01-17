# Generated by Django 4.2.7 on 2023-11-06 06:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drachar', '0034_auto_20230520_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dossier',
            name='proprietaire',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name='possede_dossier',
                to=settings.AUTH_USER_MODEL,
                verbose_name='Propriétaire',
            ),
        ),
        migrations.AlterField(
            model_name='dra',
            name='contact_livraison',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT, to='drachar.contactlivraison', verbose_name='contact pour la livraison'
            ),
        ),
        migrations.AlterField(
            model_name='dra',
            name='num_dossier',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='drachar.dossier',
                verbose_name='Dossier de travail',
            ),
        ),
    ]
