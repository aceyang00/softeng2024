from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Post

class TestView(TestCase):
    def setUp(self):
        # 클라이언트 생성
        self.client = Client()

        # 테스트 사용자 생성
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')

    def test_post_list(self):
        # 포스트 목록 페이지 요청
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        # 페이지 HTML 파싱
        soup = BeautifulSoup(response.content, 'html.parser')

        # 페이지 제목 검증
        self.assertEqual(soup.title.text, 'Blog')

        # 메인 영역 검증 (게시물이 없을 경우)
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)
        self.assertEqual(Post.objects.count(), 0)

        # 테스트용 게시물 생성
        post_001 = Post.objects.create(
            title='첫 번째 포스트입니다.',
            content='Hello World. We are the world.',
            author=self.user_trump
        )
        post_002 = Post.objects.create(
            title='두 번째 포스트입니다.',
            content='1등이 전부는 아니잖아요?',
            author=self.user_obama
        )
        self.assertEqual(Post.objects.count(), 2)

        # 포스트 목록 페이지 요청 (게시물이 있을 경우)
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        # 메인 영역 검증 (게시물이 있는 경우)
        main_area = soup.find('div', id='main-area')
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        # 작성자 정보 검증
        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)
# Create your tests here.
