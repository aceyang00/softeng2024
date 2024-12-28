from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator

from carbon.models import AgriculturalMaterial
from community.models import BlogPost, Comment
from community.forms import BlogPostForm, CommentForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm

# 게시글 편집
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
    return render(request, 'community/blog_form.html', {'form': form, 'post': post})

# 게시글 삭제
@login_required
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.user != post.author:
        return redirect('community:blog_detail', pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('community:blog_list')
    return render(request, 'community/blog_confirm_delete.html', {'post': post})

@login_required
def most_liked_post_api(request):
    """좋아요 수가 가장 많은 게시물 반환"""
    most_liked_post = (
        BlogPost.objects.annotate(total_likes=Count('likes'))
        .order_by('-total_likes', '-created_at')
        .first()
    )
    if most_liked_post:
        data = {
            'id': most_liked_post.id,
            'title': most_liked_post.title,
            'likes': most_liked_post.likes.count(),
            'url': f"/community/blog/{most_liked_post.id}/",
        }
    else:
        data = None

    return JsonResponse({'most_liked_post': data})

def register(request):
    """회원가입"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'community/register.html', {'form': form})


@login_required
def profile(request, username):
    """사용자 프로필"""
    user = get_object_or_404(User, username=username)
    return render(request, 'community/profile.html', {'user': user})


@login_required  # 로그인한 사용자만 접근 가능하도록 제한
def home(request):
    # 현재 로그인한 사용자
    user = request.user

    # 현재 사용자와 연결된 농자재만 가져오기
    materials = AgriculturalMaterial.objects.filter(user=user)

    # 좋아요가 가장 많은 게시물 (동점이면 최신 게시물 우선)
    most_liked_post = (
        BlogPost.objects.annotate(total_likes=Count('likes'))
        .order_by('-total_likes', '-created_at')
        .first()
    )

    # 컨텍스트 데이터 전달
    context = {
        'materials': materials,
        'most_liked_post': most_liked_post,
    }
    return render(request, 'home.html', context)

@login_required
def calculate(request):
    materials = AgriculturalMaterial.objects.filter(user=request.user)
    return render(request, 'carbon/calculate.html', {'materials': materials})

@login_required
def blog_list(request):
    """블로그 목록"""
    search_query = request.GET.get('search', '')
    category = request.GET.get('category', '')

    posts = BlogPost.objects.all()
    if search_query:
        posts = posts.filter(title__icontains=search_query)
    if category:
        posts = posts.filter(category=category)

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


@login_required
def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = Comment.objects.filter(blog_post=post, parent=None).prefetch_related('replies')

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
    })


@login_required
def like_post(request, post_id):
    """좋아요 추가/취소"""
    if request.method == 'POST':
        post = get_object_or_404(BlogPost, id=post_id)
        liked = False
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
            liked = True

        return JsonResponse({
            'status': 'success',
            'liked': liked,
            'likes': post.likes.count()
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def blog_create(request):
    """블로그 작성"""
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('community:blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'community/blog_form.html', {'form': form})


@login_required
def blog_edit(request, pk):
    """블로그 수정"""
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


@login_required
def add_reply(request, pk):
    parent_comment = get_object_or_404(Comment, pk=pk)  # 대댓글의 부모 댓글
    blog_post = parent_comment.blog_post  # 부모 댓글이 속한 게시글

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.blog_post = blog_post  # 대댓글의 게시글 설정
            reply.parent = parent_comment  # 대댓글의 부모 댓글 설정
            reply.author = request.user  # 대댓글 작성자
            reply.save()
            return redirect('community:blog_detail', pk=blog_post.pk)
    else:
        form = CommentForm()

    return render(request, 'community/comment_reply_form.html', {'form': form, 'comment': parent_comment})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author or request.user == comment.blog_post.author:
        comment.delete()
    return redirect('community:blog_detail', pk=comment.blog_post.pk)
