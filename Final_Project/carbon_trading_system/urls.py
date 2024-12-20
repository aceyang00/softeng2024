from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    # 관리자 페이지
    path('admin/', admin.site.urls),

    # 메인 홈 페이지
    path('', TemplateView.as_view(template_name="home.html"), name='home'),

    # 탄소 거래 앱 URL 연결
    path('carbon/', include('carbon.urls')),

    # 커뮤니티 앱 URL 연결
    path('community/', include('community.urls')),

    # 인증 관련 URL
    path('login/', auth_views.LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]
