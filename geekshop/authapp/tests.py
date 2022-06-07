from django.conf import settings
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
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertEqual(response.title, 'главная')
        self.assertNotContains(response, 'Пользователь', status_code=200)
        self.client.login(username='tarantino', password='geekshop')
        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
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

    def test_user_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'Регистрация')
        self.assertTrue(response.context['user'].is_anonymous)
        new_user_data = {
            'username': 'samuel',
            'first_name': 'Сэмюэл',
            'last_name': 'Джексон',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'samuel@geekshop.local',
            'age': '23'
        }
        response = self.client.post('/auth/register/', new=new_user_data)
        self.assertEqual(response.status_code, 302)
        new_user = ShopUser.objects.get(username=new_user_data['username'])
        activation_url = f'{settings.DOMAIN_NAME}/auth/verify/' \
                         f'{new_user_data["email"]}/' \
                         f'{new_user.activation_key}/'
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 302)
        self.client.login(username=new_user_data['username'],
                          password=new_user_data['password1'])
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        response = self.client.get('/')
        self.assertContains(response, text=new_user_data['first_name'],
                            status_code=200)


    def test_user_logout(self):
        self.client.login(username='tarantino', password='geekshop')
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context['user'].is_anonymous)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)

    def test_user_wrong_register(self):
        new_user_data = {
            'username': 'teen',
            'first_name': 'Мэри',
            'last_name': 'Поппинс',
            'password1': 'geekbrains',
            'password2': 'geekbrains',
            'email': 'samuel@geekshop.local',
            'age': '17'
        }
        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'register_form', 'age', 'Вы слишком молоды!')