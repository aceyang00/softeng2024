from django.urls import path
from . import views
from .views import home_view


app_name = 'community'


class BlogDetailView:
    pass


urlpatterns = [
    # 블로그 관련 URL
    path('', views.blog_list, name='blog_list'),
    path('<int:pk>/', views.blog_detail, name='blog_detail'),

    path('', home_view, name='home'),  # 홈 URL에 View 연결

    path('create/', views.blog_create, name='blog_create'),
    path('<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),

    # 회원가입 URL
    path('register/', views.register, name='register'),
]
