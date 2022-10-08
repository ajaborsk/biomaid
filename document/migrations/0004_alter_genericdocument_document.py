# Generated by Django 3.2.3 on 2021-06-15 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0003_auto_20210615_0703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericdocument',
            name='document',
            field=models.ForeignKey(
                default=1, on_delete=django.db.models.deletion.PROTECT, related_query_name='marche', to='document.document'
            ),
            preserve_default=False,
        ),
    ]
