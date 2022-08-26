from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from posts.models import Post, Group
from django.urls import reverse
from django import forms

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
        """ VIEW | view-классы используют ожидаемые HTML-шаблоны """
        templates_page_names = {
            reverse(
                'posts:index'
            ): 'posts/index.html',
            reverse(
                'posts:group', kwargs={'slug': self.group.slug}
            ): 'posts/group_list.html',
            reverse(
                'posts:profile', kwargs={'username': self.user.username}
            ): 'posts/profile.html',
            reverse(
                'posts:post_detail', kwargs={'post_id': self.post.pk}
            ): 'posts/post_detail.html',
            reverse(
                'posts:post_create'
            ): 'posts/post_create.html',
            reverse(
                'posts:post_edit', kwargs={'post_id': self.post.pk}
            ): 'posts/post_create.html',
        }
        for reverse_name, template in templates_page_names.items():
            with self.subTest(template=template):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_content(self):
        """ VIEW | Тестируем контент в context на странице index """
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_group_title_0 = first_object.group.title
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        self.assertEqual(post_group_title_0, 'test_group')
        self.assertEqual(post_text_0, 'Test text post №13')
        self.assertEqual(post_author_0, 'auth')

    def test_profile_content(self):
        """ VIEW | Тестируем контент в context на странице profile """
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user.username})
        )
        first_object = response.context['page_obj'][0]
        post_group_title_0 = first_object.group.title
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        self.assertEqual(post_group_title_0, 'test_group')
        self.assertEqual(post_text_0, 'Test text post №13')
        self.assertEqual(post_author_0, 'auth')

    def test_group_list_content(self):
        """ VIEW | Тестируем контент в context на странице group """
        response = self.authorized_client.get(
            reverse('posts:group', kwargs={'slug': self.group.slug})
        )
        first_object = response.context['page_obj'][0]
        post_group_title_0 = first_object.group.title
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        post_description_0 = first_object.group.description
        self.assertEqual(post_group_title_0, 'test_group')
        self.assertEqual(post_text_0, 'Test text post №13')
        self.assertEqual(post_author_0, 'auth')
        self.assertEqual(post_description_0, 'test_description')

    def test_post_detail(self):
        """ VIEW | Тестируем контент в context на странице поста """
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        )
        first_object = response.context['post']
        post_group_title_0 = first_object.group.title
        post_text_0 = first_object.text
        post_author_0 = first_object.author.username
        self.assertEqual(post_group_title_0, 'test_group')
        self.assertEqual(post_text_0, 'Test text post №13')
        self.assertEqual(post_author_0, 'auth')

    def test_new_post_context(self):
        """ Страница НОВОГО поста с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_edit_context(self):
        """ Страница РЕДАКТИРОВАНИЯ поста с правильным контекстом."""
        response = self.authorized_client.get(
            reverse(
                'posts:post_edit', kwargs={'post_id': self.post.pk}
            )
        )
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_first_page_contains_ten_records(self):
        """ VIEW | Проверка: количество постов на первой странице равно 10. """
        response = self.client.get(reverse('posts:index'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records(self):
        """ VIEW | Проверка: на второй странице должно быть три поста. """
        response = self.client.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_group_list_contains_ten_records(self):
        """ VIEW | Проверка: количество постов в group_list равно 10. """
        response = self.client.get(
            reverse(
                'posts:group', kwargs={'slug': self.group.slug}
            )
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_group_list_contains_three_records(self):
        """ VIEW | Проверка: количество постов в group_list равно 3. """
        response = self.client.get(
            reverse(
                'posts:group', kwargs={'slug': self.group.slug}
            ) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_profile_contains_ten_records(self):
        """ VIEW | Проверка: количество постов в group_list равно 10. """
        response = self.client.get(
            reverse(
                'posts:profile', kwargs={'username': self.user.username}
            )
        )
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_profile_contains_three_records(self):
        """ VIEW | Проверка: количество постов в group_list равно 3. """
        response = self.client.get(
            reverse(
                'posts:profile', kwargs={'username': self.user.username}
            ) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj']), 3)
