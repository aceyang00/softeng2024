# Generated by Django 5.1.4 on 2024-12-22 09:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("community", "0003_blogpost_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="blog_images/"),
        ),
    ]
