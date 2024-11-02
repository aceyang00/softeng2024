import csv
import os
import csv
from django.conf import settings
from itertools import zip_longest
from django.shortcuts import render
import pandas as pd

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

# def blog_list(request):
#     csv_path = os.path.join(settings.BASE_DIR, 'single_pages', 'static', 'single_pages', 'data', 'blog_content.csv')
#
#     posts = []
#     try:
#         df = pd.read_csv(csv_path, encoding='utf-8')  # CSV 파일을 pandas로 읽기
#         for _, row in df.iterrows():
#             posts.append({'title': row['title'], 'content': row['content']})
#     except Exception as e:
#         print(f"Error loading CSV file: {e}")
#
#     grouped_posts = list(zip_longest(*[iter(posts)] * 3, fillvalue=None))
#     return render(request, 'single_pages/blog.html', {'grouped_posts': grouped_posts})
def blog_list(request):
    # CSV 파일 경로 설정
    csv_path = os.path.join(settings.BASE_DIR, 'static', 'single_pages', 'data', 'blog_content.csv')

    blog = []
    try:
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                blog.append(row)
    except FileNotFoundError:
        print("sd")
    return render(request, 'single_pages/blog.html', {'error': 'CSV 파일을 찾을 수 없습니다.'})

    grouped_posts = list(zip_longest(*[iter(posts)] * 3, fillvalue=None))
    return render(request, 'single_pages/blog.html', {'grouped_posts': grouped_posts})