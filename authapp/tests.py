from django.test import TestCase
from django.test.client import Client
from authapp.models import ShopUser
from django.core.management import call_command


class TestUserManagement(TestCase):
    username = 'tarantino'
    email = 'django2@tarantino.local'
    password = 'geekbrains'
    super_username = 'django2'
    super_email = 'django2@geekshop.local'
    super_password = 'geekbrains'

    def setUp(self):
        # call_command('flush', '--noinput')
        # call_command('loaddata', 'test_db.json')
        self.client = Client()
        self.superuser = ShopUser.objects.create_superuser(self.super_username, self.super_email, self.super_password)
        self.user = ShopUser.objects.create_user(self.username, self.email, self.password)

    def test_user_login(self):
        # главная без логина
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.context['title'], 'Главная')
        self.assertNotContains(response, 'Пользователь', status_code=200)
        # self.assertNotIn('Пользователь', response.content.decode())

        # данные пользователя
        self.client.login(username=self.username, password=self.password)

        # логинимся
        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.user)

        # # главная после логина
        # response = self.client.get('/')
        # self.assertContains(response, 'Пользователь', status_code=200)
        # self.assertEqual(response.context['user'], self.user)
        # # self.assertIn('Пользователь', response.content.decode())
        #
        # # разлогиниваемся
        # self.client.logout()
        # response = self.client.get('/')
        # self.assertTrue(response.context['user'].is_anonymous)
