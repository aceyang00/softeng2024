from django.db import models
from django.contrib.auth.models import User

# 블로그 글 모델



from django.db import models

from django.db import models
from django.contrib.auth.models import User

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)  # 카테고리 추가
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)  # 이미지 필드 추가

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
