# Generated by Django 3.2.3 on 2021-06-15 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marche', '0003_auto_20210606_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lot',
            name='documents',
        ),
        migrations.DeleteModel(
            name='Document',
        ),
        migrations.DeleteModel(
            name='DocumentLink',
        ),
    ]
