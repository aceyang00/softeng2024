from django.urls import path # Ensure include is imported
from . import views


app_name = 'carbon'

urlpatterns = [
    path('trade/', views.trade, name='trade'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('calculate/', views.calculate, name='carbon_calculate'),
    path('calculate/', views.calculate, name='calculate'),  # Ensure the name is 'calculate'
    path('least_stocked_material/', views.least_stocked_material, name='least_stocked_material'),

]
