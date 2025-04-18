# Generated by Django 5.0.6 on 2024-06-06 16:19

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0008_item_item_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="mission",
            name="document",
            field=models.FileField(blank=True, null=True, upload_to="mission_pdfs/"),
        ),
        migrations.AddField(
            model_name="mission",
            name="mission_image",
            field=models.ImageField(
                blank=True, default=False, null=True, upload_to="images/"
            ),
        ),
        migrations.AlterField(
            model_name="item",
            name="description",
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name="mission",
            name="description",
            field=ckeditor.fields.RichTextField(),
        ),
    ]
