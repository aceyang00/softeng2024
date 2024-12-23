from django import forms
from .models import BlogPost, Comment

class BlogPostForm(forms.ModelForm):
    CATEGORY_CHOICES = [
        ('fruit', 'Fruit'),
        ('vegetable', 'Vegetable'),
        ('grain', 'Grain'),
        ('other', 'Other'),
    ]

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False,  # 선택 사항
        label="카테고리",
    )

    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'category', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력하세요'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': '내용을 입력하세요'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'title': '제목',
            'content': '내용',
            'image': '이미지 업로드',
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '댓글을 입력하세요...'
            }),
        }
        labels = {
            'content': '',
        }
