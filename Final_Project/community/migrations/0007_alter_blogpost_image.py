# Generated by Django 5.1.4 on 2024-12-23 11:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("community", "0006_alter_blogpost_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpost",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="posts/"),
        ),
    ]
