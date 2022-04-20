from django.shortcuts import render


def products(request):
    return render(request, 'mainapp/products.html')


def index():
    return None


def contacts():
    return None