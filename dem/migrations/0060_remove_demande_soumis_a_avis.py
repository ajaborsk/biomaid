# Generated by Django 3.2.12 on 2022-03-26 11:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0059_auto_20220326_1055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demande',
            name='soumis_a_avis',
        ),
    ]
