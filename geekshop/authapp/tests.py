from django.test import TestCase
from django.test.client import Client
from django.core.management import call_command

from authapp.models import ShopUser


class TestUserManagement(TestCase):
    def SetUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'test_db.json')
        self.client = Client()
        self.superuser = ShopUser.objects.create_superuser('django2',
                                                           'django2@geekshop.local',
                                                           'geekbrains',
                                                           )
        self.user = ShopUser.objects.create_user('tarantino',
                                                 'tarantino@geekshop.local',
                                                 'geekbrains',
                                                )
        self.user_with__first_name = ShopUser.objects.create_user('uma',
                                                                  'uma@geekshop.local',
                                                                  'geekbrains',
                                                                  first_name='turman',
                                                 )

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonimous)
        self.assertEqual(response.title, 'главная')
        self.assertNotContains(response, 'Пользователь', status_code=200)

        self.client.login(username='tarantino', password='geekshop')
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonimous)
        self.assertFalse(response.context['user'], self.user)

    def test_basket_login_redirect(self):
        response = self.client.get('/basket/')
        self.assertEqual(response.url, '/auth/login/?next=/basket/')
        self.assertEqual(response.status_code, 302)     #код редиректа

        self.client.login(username='tarantino', password='geekshop')
        response = self.client.get('/basket/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['basket']), [])
        self.assertEqual(response.request['PATH_INFO'], '/basket/')
        self.assertIn('Ваша корзина, Пользователь', response.content.decode())

    def test_user_logout(self):
