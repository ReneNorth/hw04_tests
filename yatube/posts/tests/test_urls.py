from tokenize import group
from django.contrib.auth import get_user_model
from django.test import TestCase, Client


from posts.models import Post, Group

User = get_user_model()


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user = User.objects.create(username='auth')
        cls.group = Group.objects.create(
            title='test_group',
            slug='any_slug',
            description='test_description',
        )

        cls.post = Post.objects.create(
            text='test text first post',
            author=cls.user,
            group=cls.group,
        )
        
        cls.user2 = User.objects.create(username='nonauthor')
        
        cls.post2 = Post.objects.create(
            text='test text second post',
            author=cls.user2,
            group=cls.group,
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.get(username='auth')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        


    def test_urls_authorized_author(self):
        template_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{self.group.slug}/',
            'posts/profile.html': f'/profile/{self.user.username}/',
            'posts/post_detail.html': f'/posts/{self.post.pk}/',
            'posts/post_detail.html': f'/posts/{self.post.pk}/edit',
            'posts/post_create.html': '/create/',
            'posts/post_create.html': '/unexisting_page/',
        }
        
        for template, address in template_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)


    def test_urls_not_authorized(self):
        template_url_names = {
            'posts/index.html': '/',
            # 'posts/post_create.html': '/create/',
        }
        for template, address in template_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
                
    def test_404_works(self):
        non_exist_page = '/unexisting_page/'
        response = self.guest_client.get(non_exist_page)
        self.assertEqual(response.status_code, 404)
        
        response = self.authorized_client.get(non_exist_page)
        self.assertEqual(response.status_code, 404)


# перепроверить, низкая уверенность что правильно
    def non_author_access_edit(self):
        response = self.authorized_client.get('/posts/{self.post2.pk}/edit')
        self.assertEqual(response.status_code, 302)
   




#
# неясно как отработать кейс доступа для не-автора
#     def setUp(self):
#         self.user = User.objects.get(username='nonauthor')
#         self.authorized_client_nonauthor = Client()
#         self.authorized_client_nonauthor.force_login(self.user)
#     
#     def test_only_author(self):
#         template_url_name = {
#             'posts/post_detail.html': f'/posts/{self.post.pk}/edit',
#         }
        
        
     
        
        # def test_task_list_url_exists_at_desired_location(self):
#        """Страница /task/ доступна авторизованному пользователю."""
        # response = self.authorized_client.get('/task/')
        # self.assertEqual(response.status_code, 200)