# Generated by Django 5.1.4 on 2024-12-23 13:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("carbon", "0003_alter_agriculturalmaterial_options_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="agriculturalmaterial",
            options={"verbose_name": "농자재", "verbose_name_plural": "농자재 목록"},
        ),
        migrations.AddField(
            model_name="agriculturalmaterial",
            name="threshold",
            field=models.IntegerField(default=5, verbose_name="알림 임계값"),
        ),
        migrations.AddField(
            model_name="agriculturalmaterial",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="사용자",
            ),
        ),
        migrations.AlterField(
            model_name="agriculturalmaterial",
            name="name",
            field=models.CharField(max_length=100, verbose_name="농자재 이름"),
        ),
        migrations.AlterField(
            model_name="agriculturalmaterial",
            name="quantity",
            field=models.IntegerField(default=0, verbose_name="재고 수량"),
        ),
        migrations.AlterUniqueTogether(
            name="agriculturalmaterial",
            unique_together={("user", "name")},
        ),
    ]
