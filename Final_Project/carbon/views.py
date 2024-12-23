from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AgriculturalMaterial
from django.contrib.auth.models import User

@login_required
def trade(request):
    return render(request, 'carbon/trade.html')

@login_required
def dashboard(request):
    return render(request, 'carbon/dashboard.html')

@login_required
def calculate(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                try:
                    material_id = int(key.replace('quantity_', ''))
                    material = AgriculturalMaterial.objects.get(id=material_id)
                    material.quantity = int(value)
                    material.save()
                except (ValueError, AgriculturalMaterial.DoesNotExist):
                    continue

    materials = AgriculturalMaterial.objects.all()
    return render(request, 'carbon/calculate.html', {'materials': materials})