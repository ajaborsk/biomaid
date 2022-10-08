#  Copyright (c)
#  Copyright (c)

# Generated by Django 4.0.4 on 2022-05-21 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('drachar', '0021_rename_expert_previsionnel_expert_ext'),
    ]

    operations = [
        migrations.AddField(
            model_name='previsionnel',
            name='expert',
            field=models.ForeignKey(db_column='expert_user', blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
