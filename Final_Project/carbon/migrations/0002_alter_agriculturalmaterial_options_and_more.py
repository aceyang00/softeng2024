# Generated by Django 5.1.4 on 2024-12-22 10:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("carbon", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="agriculturalmaterial",
            options={"verbose_name": "농자재", "verbose_name_plural": "농자재 목록"},
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
        migrations.AlterField(
            model_name="agriculturalmaterial",
            name="threshold",
            field=models.IntegerField(default=5, verbose_name="알림 임계값"),
        ),
    ]
