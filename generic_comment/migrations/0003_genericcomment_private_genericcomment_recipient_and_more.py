# Generated by Django 4.0 on 2023-04-27 11:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0082_programme_limit'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('generic_comment', '0002_alter_genericcomment_object_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericcomment',
            name='private',
            field=models.BooleanField(default=False, verbose_name='Privé'),
        ),
        migrations.AddField(
            model_name='genericcomment',
            name='recipient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='recipient_comments', to='common.user', verbose_name='Destinataire'),
        ),
        migrations.AlterField(
            model_name='genericcomment',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype'),
        ),
        migrations.AlterField(
            model_name='genericcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='common.user', verbose_name='Rédacteur'),
        ),
    ]