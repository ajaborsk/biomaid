# Generated by Django 3.2.3 on 2021-06-14 20:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('physical_path', models.CharField(max_length=2048)),
                ('logical_path', models.CharField(max_length=2048)),
                ('description', models.TextField(blank=True, null=True)),
                ('sha1_hash', models.CharField(blank=True, max_length=2048, null=True)),
                ('mime_type', models.CharField(blank=True, max_length=2048, null=True)),
                ('creation', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('modification', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('desactivation', models.DateTimeField(blank=True, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GenericDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Remarque sur le lien (facultatif)')),
                ('creation_datetime', models.DateTimeField(auto_now_add=True, verbose_name='date de création')),
                ('modification_datetime', models.DateTimeField(auto_now=True, verbose_name='date de modification')),
                ('desactivation_datetime', models.DateTimeField(blank=True, null=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
                (
                    'document',
                    models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='document.document'),
                ),
                (
                    'user',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Créateur du lien'
                    ),
                ),
            ],
        ),
    ]
