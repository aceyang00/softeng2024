from django.db import models
from django.contrib.auth.models import User
import os
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser


def upload_to(instance, filename):
    # 파일 이름과 확장자를 분리
    name, ext = os.path.splitext(filename)
    # 슬러그 형태로 파일 이름 변환 (한글 → 영어)
    return f'blog_images/{slugify(name)}{ext}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(upload_to='profiles/', default='profiles/default.png')

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)  # 파일 이름 처리

    def save(self, *args, **kwargs):
        if not self.category:  # 카테고리가 비어 있으면 None 설정
            self.category = 'None'
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title





# 댓글 모델
class Comment(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.blog_post}"
