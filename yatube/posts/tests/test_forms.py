from urllib import response
from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase, Client, override_settings
from posts.models import Post, Group
from django.urls import reverse



import shutil
import tempfile

from posts.forms import PostForm, PostEditForm
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile



User = get_user_model()
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

class PostFormsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.group = Group.objects.create(
            title='test_group1',
            slug='any_slug1',
            description='test_description1',
        )
        #cls.group2 = Group.objects.create(
        #    title='test_group2',
        #    slug='any_slug2',
        #    description='test_description2',
        #)
       
        cls.post = Post.objects.create(
            text='test text first post',
            author=cls.user,
            group=cls.group,
        )
        #cls.user2 = User.objects.create(username='nonauthor')
        #cls.post2 = Post.objects.create(
        #    text='test text second post',
        #    author=cls.user2,
        #    group=cls.group2,
        #)

        cls.form = PostForm()

        #count = 0
        #for i in range(0, 13):
        #    count += 1
        #    cls.post = Post.objects.create(
        #        text=f'Test text post №{count}',
        #        author=cls.user,
        #        group=cls.group,
        #    )
    
    #def tearDownClass(cls):
    #    super().tearDownClass()
    #    shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)
    
    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        
        
    def test_create_post(self):
        """Валидная форма создает новый пост."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
            # 'author': f'{self.user.username}'
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'), data=form_data, follow=True
        )
        self.assertTrue(Post.objects.filter(
            text='Тестовый текст',
        ).exists()
        )
        self.assertEqual(Post.objects.count(), posts_count+1)


    def test_edit_post(self):
        """ Проверка редактирования поста. """
        
        form_data = {
            'text': 'CHANGED Тестовый текст',
        }
        
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=(1,)), data=form_data, follow=True
        )
        
        self.assertTrue(Post.objects.filter(
            text='CHANGED Тестовый текст',
        ).exists()
        )