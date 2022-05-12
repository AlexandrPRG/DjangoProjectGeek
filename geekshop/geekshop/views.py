from django.shortcuts import render

from basketapp.models import Basket
from mainapp.models import Product


def index(request):
    product = Product.objects.all()[:4]
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    context = {
        'title': 'главная',
        'products': product,
        'basket': basket,
    }
    return render(request, 'geekshop/index.html', context)


def contacts(request):
    basket = []
    if request.user.is_authenticated:
        basket = Basket.objects.filter(user=request.user)
    context = {
        'title': 'контакты',
        'basket': basket,
    }
    return render(request, 'geekshop/contact.html', context)
