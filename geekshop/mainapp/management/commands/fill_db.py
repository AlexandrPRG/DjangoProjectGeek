from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
import os
import json
from mainapp.models import ProductCategory, Product

JSON_PATH = 'mainapp/jsons'


def load_from_json(file_name):
    with(os.path.join(JSON_PATH, file_name + '.json'), 'r') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('category')
        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()
        products = load_from_json('products')
        Product.objects.all().delete()
        for product in products:
            category_id = product['category']
            _category = ProductCategory.objects.get(category_id)
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        User.objects.create_superuser('avadmin', 'mail@django.com', '1')
