from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm

# 블로그 글 목록
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'community/blog_list.html', {'posts': posts})


# 블로그 글 상세 보기
def blog_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    comments = post.comments.all()
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
    return render(request, 'community/blog_detail.html', {'post': post, 'comments': comments, 'form': form})


# 블로그 글 작성
@login_required
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
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
            return redirect('community:blog_list')  # 회원가입 후 블로그 목록 페이지로 리디렉션
    else:
        form = UserCreationForm()
    return render(request, 'community/register.html', {'form': form})
