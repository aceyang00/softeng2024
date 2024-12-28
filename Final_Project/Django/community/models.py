from django.contrib.auth import get_user_model
from django.utils.text import slugify
import os

from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="전화번호")

    def __str__(self):
        return self.username

User = get_user_model()

# 동적으로 사용자 모델 가져오기


# Custom User Forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number']


# 농자재 관리 모델



# 파일 업로드 함수
def upload_to(instance, filename):
    name, ext = os.path.splitext(filename)  # 파일 이름과 확장자 분리
    return f'blog_images/{slugify(name)}{ext}'  # 슬러그 형태로 저장


# 블로그 관련 모델
class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="제목")
    content = models.TextField(verbose_name="내용")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="작성자")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="작성일")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="수정일")
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True, verbose_name="좋아요")
    category = models.CharField(max_length=100, null=True, blank=True, verbose_name="카테고리")
    image = models.ImageField(upload_to=upload_to, null=True, blank=True, verbose_name="이미지")

    def save(self, *args, **kwargs):
        if not self.category:
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
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.blog_post}"


# 프로필 모델
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="사용자")
    image = models.ImageField(upload_to='profiles/', default='profiles/default.png', verbose_name="프로필 이미지")

    def __str__(self):
        return f"Profile of {self.user.username}"
