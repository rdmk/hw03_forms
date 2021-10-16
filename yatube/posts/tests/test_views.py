from django import forms
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class TaskPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='test-title',
            slug='test-slug',
            description='test-decsr',
        )
        cls.user = User.objects.create_user(username='Test_user')
        cls.post = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group,
            pk='1234',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client(self.user)
        self.authorized_client.force_login(self.user)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            reverse(
                'posts:index'): 'posts/index.html',
            reverse(
                'posts:group_list',
                kwargs={'slug': 'test-slug'}): 'posts/group_list.html',
            reverse(
                'posts:profile',
                kwargs={'username': 'Test_user'}): 'posts/profile.html',
            reverse(
                'posts:post_detail',
                kwargs={'post_id': '1234'}): 'posts/post_detail.html',
            reverse(
                'posts:post_edit',
                kwargs={'post_id': '1234'}): 'posts/create_or_update.html',
            reverse(
                'posts:post_create'): 'posts/create_or_update.html'
        }
        for reverse_name, template in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        for object in response.context['page_obj']:
            post_text = object.text
            post_author = object.author
            post_group = object.group
            self.assertEqual(post_text, self.post.text)
            self.assertEqual(post_author, self.user)
            self.assertEqual(post_group, self.group)

    def test_group_page_show_correct_context(self):
        """Шаблон group сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': self.group.slug})
        )
        for object in response.context['page_obj']:
            post_title = object.group.title
            post_slug = object.group.slug
            post_description = object.group.description
            self.assertEqual(post_title, self.group.title)
            self.assertEqual(post_slug, self.group.slug)
            self.assertEqual(post_description, self.group.description)

    def test_profile_page_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': 'Test_user'})
        )
        for object in response.context['page_obj']:
            post_text = object.text
            post_author = object.author
            post_group = object.group
            self.assertEqual(post_text, self.post.text)
            self.assertEqual(post_author, self.user)
            self.assertEqual(post_group, self.group)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_detail', kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(response.context['post'].text, self.post.text)
        self.assertEqual(response.context['post'].author, self.user)
        self.assertEqual(response.context['post'].group, self.group)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:post_edit', kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(response.context['post'].text, self.post.text)
        self.assertEqual(response.context['post'].group, self.group)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.models.ModelChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)
