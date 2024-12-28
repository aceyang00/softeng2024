from django.db import models
from django.contrib.auth import get_user_model

# 사용자 모델을 동적으로 가져옴
User = get_user_model()


class AgriculturalMaterial(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="agricultural_materials",  # 역참조 이름 지정
        verbose_name="사용자"
    )
    name = models.CharField(max_length=100, verbose_name="농자재 이름")
    quantity = models.IntegerField(default=0, verbose_name="재고 수량")
    threshold = models.IntegerField(default=5, verbose_name="알림 임계값")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="등록일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    description = models.TextField(blank=True, null=True, verbose_name="설명")
    unit = models.CharField(max_length=20, default='개', verbose_name="단위")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="단가")
    category = models.CharField(
        max_length=50,
        choices=[
            ('fertilizer', '비료'),
            ('pesticide', '농약'),
            ('tool', '농기구'),
            ('seed', '종자'),
            ('other', '기타')
        ],
        default='other',
        verbose_name="카테고리"
    )

    def is_below_threshold(self):
        """재고가 임계값 이하인지 확인"""
        return self.quantity <= self.threshold

    def total_value(self):
        """총 재고 가치 계산"""
        return self.quantity * self.price

    def __str__(self):
        return f"{self.name} ({self.quantity}{self.unit})"

    class Meta:
        verbose_name = "농자재"
        verbose_name_plural = "농자재 목록"
        ordering = ['-created_at']  # 최신 등록순으로 정렬
