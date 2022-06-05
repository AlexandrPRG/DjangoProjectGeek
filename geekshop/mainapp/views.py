import random

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from basketapp.models import Basket
from .models import Product, ProductCategory
from django.contrib.auth.decorators import login_required


def product(request, pk):
    title = str(Product.objects.get(pk=pk).name)
    product = get_object_or_404(Product, pk=pk)
    links_menu_products = ProductCategory.objects.all()
    same_products = Product.objects.filter(category__pk=Product.objects.get(pk=pk).category.pk)
    # same_products = get_same_products(get_hot_product())
    # basket = get_basket(request.user)
    context = {
        'title': title,
        'product': product,
        'type': type(product),
        'links_menu_products': links_menu_products,
        'same_products': same_products,
        # 'basket': basket,
        }
    return render(request, 'mainapp/product.html', context)


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects\
        .filter(category=hot_product.category)\
        .exclude(pk=hot_product.pk)\
        .order_by('price')
    return same_products

def products(request, pk=None, page=1):
    title = 'каталог'
    links_menu_products = ProductCategory.objects.all()
    # basket = get_basket(request.user)
    products = Product.objects.all().order_by('price')
    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
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
            "products": products_paginator,
            # 'basket': basket,
            }
        return render(request, 'mainapp/products_list.html', context)
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        "links_menu_products": links_menu_products,
        "title": title,
        "same_products": same_products,
        'hot_product': hot_product,
        # 'basket': basket,
        'products': products_paginator,
        }
    return render(request, 'mainapp/products.html', context=context)
