from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Post, Group
# import pytest


User = get_user_model()


# @pytest.mark.django_db
class PostTest(TestCase):
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
        test_post = PostTest.post
        max_len = 15
        text_len = len(str(test_post))
        self.assertEqual(text_len, max_len)

    def test_group_titile(self):
        """ MODELS | Тест совпадения title """
        test_group = PostTest.group
        expected_group_name = test_group.title
        self.assertEqual(expected_group_name, str(test_group))
