from deals.models import Task
from django.contrib.auth import get_user_model
from django.http import response
from django.test import Client, TestCase

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_author_page(self):
        response = self.guest_client.get('/about/author/')
        self.assertAlmostEqual(response.status_code, 200)

    def test_tech_page(self):
        response = self.guest_client.get('/about/tech/')
        self.assertAlmostEqual(response.status_code, 200)


class TaskURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создадим запись в БД для проверки доступности адреса task/test-slug/
        Task.objects.create(
            title='Тестовый заголовок',
            text='Тестовый текст',
            slug='test-slug'
        )

    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()
        # Создаем пользователя
        self.user = User.objects.create_user(username='HasNoName')
        # Создаем второй клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(self.user)

    def test_home_url_exists_at_desired_location(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_group_slug_exists_at_desired_location(self):
        response = self.guest_client.get('/group/<slug:slug>/')
        self.assertEqual(response.status_code, 200)

    def test_profile_username_exists_at_desired_location(self):
        response = self.guest_client.get('/profile/<str:username>/')
        self.assertEqual(response.status_code, 200)

    def test_post_id_exists_at_desired_location(self):
        response = self.guest_client.get('/posts/<int:post_id>/')
        self.assertEqual(response.status_code, 200)

#    def test_post_id_edit_exists_at_desired_location(self):
        # нужно добавить свойства автора
#        response = self.authorized_client.get('/posts/<int:post_id>/edit/')
#        self.assertEqual(response.status_code, 200)


    def test_post_id_edit_exists_at_desired_location(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)
    
    def test_unexisting_page(self):
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, 404)

