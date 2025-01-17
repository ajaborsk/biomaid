# Generated by Django 3.0.7 on 2020-10-06 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0017_auto_20200929_2149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demande',
            name='cause',
            field=models.CharField(
                choices=[
                    ('RE', 'Remplacement'),
                    ('AQ', 'Augmentation de Quantité'),
                    ('EV', 'Evolution'),
                    ('TN', 'Technique Nouvelle'),
                    ('RA', 'Rachat fin de marché'),
                ],
                default='AQ',
                help_text="C'est la raison pour laquelle cette demande est faite.",
                max_length=3,
                verbose_name='Raison',
            ),
        ),
    ]
