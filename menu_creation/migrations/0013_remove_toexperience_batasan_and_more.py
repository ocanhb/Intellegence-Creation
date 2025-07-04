# Generated by Django 5.2.2 on 2025-06-26 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu_creation', '0012_datasetsent_toexperience_delete_datasetresponse_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='toexperience',
            name='batasan',
        ),
        migrations.RemoveField(
            model_name='toexperience',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='toexperience',
            name='implementasi',
        ),
        migrations.RemoveField(
            model_name='toexperience',
            name='meaningful',
        ),
        migrations.RemoveField(
            model_name='toexperience',
            name='perencanaan',
        ),
        migrations.AddField(
            model_name='toexperience',
            name='batasan_path',
            field=models.FileField(blank=True, null=True, upload_to='dokumen/'),
        ),
        migrations.AddField(
            model_name='toexperience',
            name='experience_path',
            field=models.FileField(blank=True, null=True, upload_to='dokumen/'),
        ),
        migrations.AddField(
            model_name='toexperience',
            name='implementasi_path',
            field=models.FileField(blank=True, null=True, upload_to='dokumen/'),
        ),
        migrations.AddField(
            model_name='toexperience',
            name='meaningful_path',
            field=models.FileField(blank=True, null=True, upload_to='dokumen/'),
        ),
        migrations.AddField(
            model_name='toexperience',
            name='perencanaan_path',
            field=models.FileField(blank=True, null=True, upload_to='dokumen/'),
        ),
    ]
