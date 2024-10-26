import csv
import os
from django.shortcuts import render
from itertools import zip_longest

# Create your views here.

def index_page(request):
    return render(request, 'single_pages/index.html', {'title': '홈'})

def members_page(request):
    return render(request, 'single_pages/members.html', {'title': '멤버스'})

def edu_page(request):
    return render(request, 'single_pages/edu.html', {'title': '교육과정'})

def map_page(request):
    return render(request, 'single_pages/map.html', {'title': '찾아오는 길'})

def blog_page(request):
    return render(request, 'single_pages/blog.html', {'title': '게시판'})



def blog_list(request):
    # CSV 파일 경로 설정
    csv_path = os.path.join(settings.BASE_DIR, 'static/data/blog_content.csv')

    # CSV 파일 읽기
    blog = []
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            blog.append(row)

    # 데이터를 템플릿에 전달
    return render(request, 'single_pages/blog_list.html', {'blog': blog})

    # posts = [
    #     {'title': '첫 번째 글', 'content': '이것은 첫 번째 블로그 글입니다.'},
    #     {'title': '두 번째 글', 'content': '이것은 두 번째 블로그 글입니다.'},
    #     {'title': '세 번째 글', 'content': '이것은 세 번째 블로그 글입니다.'},
    #     {'title': '네 번째 글', 'content': '이것은 네 번째 블로그 글입니다.'},
    #     {'title': '다섯 번째 글', 'content': '이것은 다섯 번째 블로그 글입니다.'},
    #     {'title': '여섯 번째 글', 'content': '이것은 여섯 번째 블로그 글입니다.'},
    #     {'title': '일곱 번째 글', 'content': '이것은 일곱 번째 블로그 글입니다.'},
    # ]

    grouped_posts = list(zip_longest(*[iter(posts)] * 3, fillvalue=None))
    return render(request, 'single_pages/blog.html', {'grouped_posts': grouped_posts})