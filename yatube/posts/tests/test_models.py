from tokenize import group
from django.contrib.auth import get_user_model
import unittest
from django.test import TestCase
from ..models import Post, Group

User = get_user_model()


class PostTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.group = Group.objects.create(
            title='test_title_1',
            slug='test_slug_1',
            description='test_desc_1',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Sed ut perspiciatis unde omnis iste natus error sit'
        )

    def test_str_post(self):
        """ MODELS | Тест вывод 15 символов поста """
        post = PostTest.post
        max_len = 15
        text_len = len(str(post))
        self.assertEqual(text_len, max_len)

    def test_group_titile(self):
        """ MODELS | Тест совпадения title """
        group = PostTest.group
        expected_group_name = group.title
        self.assertEqual(expected_group_name, str(group))
