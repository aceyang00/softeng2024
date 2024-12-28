# Generated by Django 5.1.4 on 2024-12-23 20:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AgriculturalMaterial",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="농자재 이름")),
                ("quantity", models.IntegerField(default=0, verbose_name="재고 수량")),
                ("threshold", models.IntegerField(default=5, verbose_name="알림 임계값")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="등록일"),
                ),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="수정일")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="설명"),
                ),
                (
                    "unit",
                    models.CharField(default="개", max_length=20, verbose_name="단위"),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, default=0, max_digits=10, verbose_name="단가"
                    ),
                ),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("fertilizer", "비료"),
                            ("pesticide", "농약"),
                            ("tool", "농기구"),
                            ("seed", "종자"),
                            ("other", "기타"),
                        ],
                        default="other",
                        max_length=50,
                        verbose_name="카테고리",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="agricultural_materials",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="사용자",
                    ),
                ),
            ],
            options={
                "verbose_name": "농자재",
                "verbose_name_plural": "농자재 목록",
                "ordering": ["-created_at"],
            },
        ),
    ]
