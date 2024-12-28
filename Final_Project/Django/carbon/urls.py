from django.urls import path # Ensure include is imported
from . import views


app_name = 'carbon'

urlpatterns = [
    path('trade/', views.trade, name='trade'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('calculate/', views.calculate, name='carbon_calculate'),
    path('calculate/', views.calculate, name='calculate'),  # Ensure the name is 'calculate'
    path('least_stocked_material/', views.least_stocked_material, name='least_stocked_material'),
    path('create_material/', views.create_material, name='create_material'),
    path('create/', views.create_material, name='create_material'),  # 농자재 추가 페이지

]
