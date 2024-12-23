from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AgriculturalMaterial

@receiver(post_save, sender=AgriculturalMaterial)
def send_alert(sender, instance, **kwargs):
    if instance.is_below_threshold():
        print(f"[알림] '{instance.name}'의 재고가 {instance.quantity}개로 임계값 이하입니다!")
