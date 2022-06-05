import random

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.functional import cached_property
from basketapp.models import Basket
from .models import Product, ProductCategory
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.conf import settings
from django.views.decorators.cache import cache_page, never_cache


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


@never_cache
def product(request, pk):
    title = str(Product.objects.get(pk=pk).name)
    product = get_product(pk)
    links_menu_products = get_links_menu()
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


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category {pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
            return category
        else:
            return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, products)
            return products
        else:
            return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product {pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
            return product
        else:
            return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
            return products
        else:
            return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = 'products_in_category_ordered_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category=pk, is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
            return products
        else:
            return Product.objects.filter(category=pk, is_active=True, category__is_active=True).order_by('price')


def get_hot_product():
    products = Product.objects.all()
    return random.sample(list(products), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects\
        .filter(category=hot_product.category)\
        .exclude(pk=hot_product.pk)\
        .order_by('price')
    return same_products


@cache_page(3600)
def products(request, pk=None, page=1):
    title = 'каталог'
    links_menu_products = get_links_menu()
    # basket = get_basket(request.user)
    products = get_products_ordered_by_price()
    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    if pk is not None:
        if pk == 0:
            products = get_products_ordered_by_price()
            category = {"name": 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = get_products_in_category_ordered_by_price(pk)
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
