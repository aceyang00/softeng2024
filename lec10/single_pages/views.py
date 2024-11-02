import os
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from itertools import zip_longest

# Create your views here.


def index_page(request):
    return render(request, "single_pages/index.html", {"title": "홈"})

def members_page(request):
    return render(request, "single_pages/members.html", {"title": "멤버스"})

def edu_page(request):
    return render(request, "single_pages/edu.html", {"title": "교육과정"})

def map_page(request):
    return render(request, "single_pages/map.html", {"title": "찾아오는 길"})

def blog_list_no(request):
    return render(request, "single_pages/blog.html", {"title": "게시판"})

# def blog_list(request):
#     posts = [
#         {"title": "첫 번째 글", "content": "이것은 첫 번째 블로그 글입니다."},
#         {"title": "두 번째 글", "content": "이것은 두 번째 블로그 글입니다."},
#         {"title": "세 번째 글", "content": "이것은 세 번째 블로그 글입니다."},
#         {"title": "네 번째 글", "content": "이것은 네 번째 블로그 글입니다."},
#         {"title": "다섯 번째 글", "content": "이것은 다섯 번째 블로그 글입니다."},
#         {"title": "여섯 번째 글", "content": "이것은 여섯 번째 블로그 글입니다."},
#         {"title": "일곱 번째 글", "content": "이것은 일곱 번째 블로그 글입니다."},
#     ]
#
#     grouped_posts = list(zip_longest(*[iter(posts)] * 3, fillvalue=None))
#     return render(request, "single_pages/blog.html", {"grouped_posts": grouped_posts})

def blog_list(request):
    csv_path = os.path.join(settings.BASE_DIR, 'single_pages', 'static', 'single_pages', 'data', 'blog_content.csv')

    posts = []
    try:
        df = pd.read_csv(csv_path, encoding='utf-8')  # CSV 파일을 pandas로 읽기
        for _, row in df.iterrows():
            posts.append({'title': row['title'], 'content': row['content']})
    except Exception as e:
        print(f"Error loading CSV file: {e}")

    grouped_posts = list(zip_longest(*[iter(posts)] * 3, fillvalue=None))
    return render(request, 'single_pages/blog.html', {'grouped_posts': grouped_posts})
