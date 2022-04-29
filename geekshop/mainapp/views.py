from django.shortcuts import render
from .models import Product


def products(request):
    links_menu_products = [
        {'href': '', 'name': 'все'},
        {'href': '', 'name': 'дом'},
        {'href': '', 'name': 'офис'},
        {'href': '', 'name': 'модерн'},
        {'href': '', 'name': 'классика'},
    ]
    context = {
        "links_menu_products": links_menu_products,
        "title": 'каталог',
        "object": Product.objects.get(id=1)
    }
    return render(request, 'mainapp/products.html', context=context)
