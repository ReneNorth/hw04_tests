from django.contrib.auth import get_user_model
from django.db import models
from django.test import TestCase, Client
from posts.models import Post, Group
from django.urls import reverse

User = get_user_model()


class PostViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.group = Group.objects.create(
            title='test_group',
            slug='any_slug',
            description='test_description',
        )

        count = 0
        for i in range(0, 13):
            count += 1
            cls.post = Post.objects.create(
                text=f'Test text post №{count}',
                author=cls.user,
                group=cls.group,
            )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_about_page_uses_correct_template2(self):
        """Тестируем URL -> шаблон"""
        templates_page_names = {
            'posts/index.html': reverse(
                'posts:index'
            ),
            'posts/group_list.html': reverse(
                'posts:group', kwargs={'slug': f'{self.group.slug}'}
            ),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': f'{self.user.username}'}
            ),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': f'{self.post.pk}'}
            ),
            'posts/post_create.html': reverse(
                'posts:post_create'
            ),
            'posts/post_create.html': reverse(
                'posts:post_edit', kwargs={'post_id': f'{self.post.pk}'}
            ),
        }
        for template, reverse_name in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


        
    def test_index_content(self):
        """Тестируем контент в context на странице index"""
        response = self.authorized_client.get(reverse('posts:index'))
        # Взяли первый элемент из списка и проверили, что его содержание
        # совпадает с ожидаемым
        first_object = response.context['page_obj'][0]
        task_group_title_0 = first_object.group.title
        task_text_0 = first_object.text
        task_author_0 = first_object.author.username
        self.assertEqual(task_group_title_0, 'test_group')
        self.assertEqual(task_text_0, 'Test text post №13')
        self.assertEqual(task_author_0, 'auth')

    def test_index_context(self):
        """ This test doesn't work yet / how to get the object class """
        response = self.authorized_client.get(reverse('posts:index'))
        value = 'text'
        expected = models.CharField
        form_field = response.context.get('page_obj')
        self.assertIsInstance(form_field, expected)

    def test_first_page_contains_ten_records(self):
        """ Проверка: количество постов на первой странице равно 10. """
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        """ Проверка: на второй странице должно быть три поста. """

        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)
