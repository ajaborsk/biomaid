# Generated by Django 4.2.7 on 2024-01-23 16:41

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('marche', '0013_alter_lot_code_four'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='exceptionmarche',
            managers=[
                ('records', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='familleachat',
            managers=[
                ('records', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='lot',
            managers=[
                ('records', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='marche',
            managers=[
                ('records', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='procedure',
            managers=[
                ('records', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='suivi',
            managers=[
                ('records', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name='typeprocedure',
            managers=[
                ('records', django.db.models.manager.Manager()),
            ],
        ),
    ]