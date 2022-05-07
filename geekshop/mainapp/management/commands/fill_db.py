from django.core.management.base import BaseCommand
import os
import json

from authapp.models import ShopUser
from mainapp.models import ProductCategory, Product

JSON_PATH = 'mainapp/jsons'

def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), 'r', encoding='utf-8') as file:
        return json.load(file)


class Command(BaseCommand):
    def handle(self, *args, **options):
        categories = load_from_json('categories')
        ProductCategory.objects.all().delete()
        for category in categories:
            new_category = ProductCategory(**category)
            print(f'из продукткатегори{category=}')
            print(f'из продукткатегори{ProductCategory=}')
            print(f'из продукткатегори{ProductCategory(**category)=}')
            # print(f'{category=}', f'{categories=}')
            # print(f'{new_category=}', f'{ProductCategory(**category)=}')
            new_category.save()
            print(f'из продукткатегори{ProductCategory.objects.all()=}')


        products = load_from_json('products')
        Product.objects.all().delete()
        try:
            for product in products:
                category_name = product['category']
                print(f'{category_name=}')
                print(f'{ProductCategory.objects.get(id=category_name)=}')
                _category = ProductCategory.objects.get(id=category_name)
                product['category'] = _category
                mew_product = Product(**product)
                mew_product.save()
                print(f'{Product.objects.all()=}')
        except DoesNotExist:
            print(f'{category_name=}')
        finally:
            ShopUser.objects.create_superuser('avadmin', 'mail@django.com', '1', age=23)
            print(f'{ShopUser.objects.all()=}')


