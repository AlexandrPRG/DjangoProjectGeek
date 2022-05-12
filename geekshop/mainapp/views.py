from django.shortcuts import render, get_object_or_404

from basketapp.models import Basket
from .models import Product, ProductCategory


def product(request, pk):
    print(pk)
    return render(request)


def products(request, pk=None):
    title = 'каталог'
    links_menu_products = ProductCategory.objects.all()
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {"name": 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.all().filter(category__pk=pk).order_by('price')
            title = title + f': {ProductCategory.objects.get(pk=pk).name}'
        context = {
            "title": title,
            "links_menu_products": links_menu_products,
            "category": category,
            "products": products,
            'basket': basket,
            }
        return render(request, 'mainapp/products_list.html', context)
    same_products = Product.objects.all()[3:5]
    context = {
        "links_menu_products": links_menu_products,
        "title": title,
        "same_products": same_products,
        'basket': basket,
        }
    return render(request, 'mainapp/products.html', context=context)
