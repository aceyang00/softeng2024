from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import AgriculturalMaterial
from django.contrib.auth.models import User
from .forms import AgriculturalMaterialForm

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

    materials = AgriculturalMaterial.objects.filter(user=request.user)
    return render(request, 'carbon/calculate.html', {'materials': materials})
from django.http import JsonResponse
from .models import AgriculturalMaterial
from django.db import models

@login_required
def least_stocked_material(request):
    # 현재 로그인한 사용자 데이터만 필터링
    user_materials = AgriculturalMaterial.objects.filter(user=request.user).order_by('quantity')[:3]
    least_stocked = [
        {"name": material.name, "quantity": material.quantity} for material in user_materials
    ]

    return JsonResponse({"least_stocked": least_stocked})



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AgriculturalMaterialForm
from .models import AgriculturalMaterial

@login_required
def create_material(request):
    if request.method == 'POST':
        form = AgriculturalMaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.user = request.user  # 현재 로그인한 사용자와 연결
            material.save()
            return redirect('carbon:calculate')  # 저장 후 농자재 관리 페이지로 이동
    else:
        form = AgriculturalMaterialForm()
    return render(request, 'carbon/create_material.html', {'form': form})




