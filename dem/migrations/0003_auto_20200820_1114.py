# Generated by Django 3.0.5 on 2020-08-20 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0002_auto_20200820_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='avis',
            name='date_fin',
            field=models.DateTimeField(null=True, verbose_name='date de fin'),
        ),
        migrations.AlterField(
            model_name='avis',
            name='code',
            field=models.DecimalField(decimal_places=0, default=1, max_digits=5),
        ),
    ]
