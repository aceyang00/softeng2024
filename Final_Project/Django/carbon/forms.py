from django import forms
from .models import AgriculturalMaterial
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from community.models import CustomUser

class AgriculturalMaterialForm(forms.ModelForm):
    class Meta:
        model = AgriculturalMaterial
        fields = ['name', 'quantity']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '이메일을 입력하세요'})
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '전화번호를 입력하세요'})
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '사용자 이름을 입력하세요'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 비밀번호 필드 스타일링
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
        # 라벨 한글화
        self.fields['username'].label = '사용자 이름'
        self.fields['email'].label = '이메일'
        self.fields['phone_number'].label = '전화번호'
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('이미 사용중인 이메일입니다.')
        return email


class CustomUserChangeForm(UserChangeForm):
    password = None  # 비밀번호 필드 제거

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': '사용자 이름',
            'email': '이메일',
            'phone_number': '전화번호',
        }