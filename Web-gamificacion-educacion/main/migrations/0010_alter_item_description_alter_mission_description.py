# Generated by Django 5.0.6 on 2024-06-07 15:58

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0009_mission_document_mission_mission_image_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="item",
            name="description",
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
        migrations.AlterField(
            model_name="mission",
            name="description",
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
