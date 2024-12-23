# Generated by Django 5.1.4 on 2024-12-23 11:02

import community.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("community", "0005_profile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to=community.models.upload_to
            ),
        ),
    ]