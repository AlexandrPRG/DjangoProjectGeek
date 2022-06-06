from django.test import TestCase
from django.core.management import call_command
from django.test.client import Client

from mainapp.models import ProductCategory, Product


class TestMainappSmoke(TestCase):
    def setUp(self):
        call_command('flush', '--noinput')
        call_command('loaddata', 'mainapp/jsons/categories.json')
        call_command('loaddata', 'mainapp/jsons/products.json')
        self.client = Client()

    def test_mainapp_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/contacts/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/products/category/0/')
        self.assertEqual(response.status_code, 200)
        for category in ProductCategory.objects.all():
            response = self.client.get(f'/products/category/{category.pk}/')
            self.assertEqual(response.status_code, 200)
        for product in Product.objects.all():
            response = self.client.get(f'/products/{product.pk}/')
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequensereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')