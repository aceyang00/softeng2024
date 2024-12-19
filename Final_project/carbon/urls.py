from django.urls import path
from . import views

app_name = 'carbon'

urlpatterns = [
    path('trade/', views.trade, name='trade'),
    path('calculate/', views.calculate, name='calculate'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
