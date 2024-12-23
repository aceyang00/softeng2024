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

    for post in posts:
        if not post.image:
            post.image = None  # 기본 이미지가 필요하면 여기에 경로를 추가할 수도 있음

    paginator = Paginator(posts, 6)
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
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Comment
from .forms import CommentForm

@login_required
def blog_detail(request, pk):
    # 현재 게시물 가져오기
    post = get_object_or_404(BlogPost, pk=pk)

    # 이전/다음 게시물 가져오기
    previous_post = BlogPost.objects.filter(id__lt=post.id).order_by('-id').first()
    next_post = BlogPost.objects.filter(id__gt=post.id).order_by('id').first()

    # 댓글 가져오기
    comments = post.comments.all()

    # 좋아요 상태 확인
    liked = request.user.is_authenticated and post.likes.filter(id=request.user.id).exists()

    # 댓글 폼 처리
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

    # 컨텍스트 데이터 전달
    return render(request, 'community/blog_detail.html', {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'comments': comments,
        'form': form,
        'liked': liked,
        'total_likes': post.likes.count(),
    })



# 좋아요 기능 - AJAX 지원
@login_required
def like_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)  # 좋아요 취소
            liked = False
        else:
            post.likes.add(request.user)  # 좋아요 추가
            liked = True

        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'likes': post.likes.count()
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


# 블로그 글 작성
@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)  # request.FILES 추가
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
        form = BlogPostForm(request.POST, request.FILES, instance=post)
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


# 사용자 프로필
def profile(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'community/profile.html', {'user': user})
