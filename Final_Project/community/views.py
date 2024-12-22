from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm



# 블로그 글 목록
@login_required

def blog_list(request):
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')

    posts = BlogPost.objects.all()
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    if category:
        posts = posts.filter(category=category)

    paginator = Paginator(posts, 6)  # 한 페이지에 6개씩 표시
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    categories = BlogPost.objects.values_list('category', flat=True).distinct()

    return render(request, 'community/blog_list.html', {
        'posts': posts,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category,
    })


# 블로그 글 상세 보기
@login_required

def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all()
    liked = False

    if request.user.is_authenticated and post.likes.filter(id=request.user.id).exists():
        liked = True

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.blog_post = post
            comment.save()
            return redirect('community:blog_detail', pk=pk)
    else:
        form = CommentForm()

    return render(request, 'community/blog_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
        'liked': liked,
        'total_likes': post.total_likes(),
    })


# 좋아요 기능
@login_required
def blog_like(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user.is_authenticated:
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})
    return JsonResponse({'error': 'You must be logged in to like posts.'}, status=403)


# 블로그 글 작성
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import BlogPostForm
from .models import BlogPost

@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)  # 이미지 처리를 위해 request.FILES 추가
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('community:blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'community/blog_form.html', {'form': form})



# 블로그 글 수정
@login_required
def blog_edit(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user != post.author:
        return redirect('community:blog_detail', pk=pk)

    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('community:blog_detail', pk=pk)
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'community/blog_form.html', {'form': form})


# 블로그 글 삭제
@login_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user != post.author:
        return redirect('community:blog_detail', pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('community:blog_list')
    return render(request, 'community/blog_confirm_delete.html', {'post': post})


# 회원가입
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # 회원가입 후 자동 로그인
            return redirect('/')  # 회원가입 후 홈 페이지로 리디렉션
    else:
        form = UserCreationForm()
    return render(request, 'community/register.html', {'form': form})
