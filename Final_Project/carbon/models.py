from django.db import models

class AgriculturalMaterial(models.Model):
    name = models.CharField(max_length=100, verbose_name="농자재 이름")
    quantity = models.IntegerField(default=0, verbose_name="재고 수량")
    threshold = models.IntegerField(default=5, verbose_name="알림 임계값")

    def is_below_threshold(self):
        return self.quantity <= self.threshold

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "농자재"
        verbose_name_plural = "농자재 목록"
