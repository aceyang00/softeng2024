from django.contrib import admin

# CustomUser 관련 코드 제거
# from .forms import CustomUserCreationForm, CustomUserChangeForm
# from community.models import CustomUser

# carbon 모델만 등록
from .models import AgriculturalMaterial

@admin.register(AgriculturalMaterial)
class AgriculturalMaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'user', 'created_at')
    list_filter = ('user',)  # 사용자별 필터링 가능

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # superuser는 모든 데이터, 일반 사용자는 자신의 데이터만 볼 수 있음
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)