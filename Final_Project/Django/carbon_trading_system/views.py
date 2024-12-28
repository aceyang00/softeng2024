from django.contrib.auth import logout
from django.shortcuts import redirect

def custom_logout(request):
    logout(request)  # 사용자 로그아웃
    return redirect('home')  # 로그아웃 후 홈 페이지로 리디렉션
