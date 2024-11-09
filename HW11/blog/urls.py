from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='blog'),  # 이 URL에 'blog'라는 이름을 추가
    path('<int:pk>/', views.PostDetail.as_view(), name='post_detail')  # 필요에 따라 이름을 추가
]
