from . import views
from django.contrib import admin  # 관리자 모듈 임포트
from django.urls import path, include  # URL 관련 모듈
from django.conf import settings  # settings.py 접근
from django.conf.urls.static import static  # 정적/미디어 파일 제공
app_name = 'community'

urlpatterns = [
    # 블로그 관련 URL
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),
    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('admin/', admin.site.urls),

    path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),

    # 회원가입 URL
    path('register/', views.register, name='register'),
]

