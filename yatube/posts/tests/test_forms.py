from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post, Group
from django.urls import reverse
from posts.forms import PostForm


User = get_user_model()


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
        cls.post = Post.objects.create(
            text='test text first post',
            author=cls.user,
            group=cls.group,
        )
        cls.form = PostForm()

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """ FORMS | Валидная форма создает новый пост."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
        }
        self.authorized_client.post(
            reverse('posts:post_create'), data=form_data, follow=True
        )
        self.assertTrue(Post.objects.filter(
            text='Тестовый текст',
        ).exists()
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post(self):
        """ FORMS | Проверка редактирования поста. """
        form_data = {
            'text': 'CHANGED Тестовый текст',
        }
        self.authorized_client.post(
            reverse(
                'posts:post_edit', args=(self.post.pk,)
            ), data=form_data, follow=True
        )
        self.assertTrue(
            Post.objects.filter(
                pk=self.post.pk, text='CHANGED Тестовый текст'
            ).exists()
        )
