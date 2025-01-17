# Generated by Django 3.0.5 on 2020-08-20 09:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dem', '0003_auto_20200820_1114'),
    ]

    operations = [
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('nom', models.CharField(max_length=30)),
                ('commentaire', models.CharField(default=None, max_length=120)),
                ('enveloppe', models.DecimalField(decimal_places=0, max_digits=10)),
                ('anteriorite', models.CharField(default=None, max_length=10)),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('date_fin', models.DateTimeField(null=True, verbose_name='date de fin')),
                ('date_modification', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('discipline', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='dem.Discipline')),
            ],
        ),
    ]
