from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def trade(request):
    return render(request, 'carbon/trade.html')

@login_required
def calculate(request):
    return render(request, 'carbon/calculate.html')

@login_required
def dashboard(request):
    return render(request, 'carbon/dashboard.html')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# 탄소 거래 페이지 (로그인 필요)
@login_required
def trade(request):
    return render(request, 'carbon/trade.html')

# 탄소 사용량 계산 페이지 (로그인 필요)
@login_required
def calculate(request):
    return render(request, 'carbon/calculate.html')
