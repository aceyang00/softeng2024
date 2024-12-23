# from django.shortcuts import render
from .models import Post
from django.views.generic import ListView, DetailView
from django.shortcuts import render
# Create your views here.

class PostList(ListView):
    model = Post
    ordering = '-pk'

# def index(request):
#     posts = Post.objects.all().order_by("-pk")
#
#     return render(
#         request,
#         "blog/index.html",
#         {
#             "posts": posts,
#         }
#     )
#

    # template_name = 'blog/index.html'

class PostDetail(DetailView):
    model = Post

# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#         request,
#         'blog/single_post_page.html',
#         {
#             "post": post,
#         }
#     )
#     template_name = 'blog/single_post_page.html'

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'post_list': posts})