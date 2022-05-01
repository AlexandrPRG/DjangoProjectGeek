from django.shortcuts import render
# from ..mainapp.models import Product
# from geekshop.mainapp.models import Product
# from ..mainapp.models import *
from mainapp.models import Product


def index(request):
    product = Product.objects.all()[:4]
    context = {
        'title': 'главная',
        'products': product,

    }
    return render(request, 'geekshop/index.html', context)

def contacts(request):
    return render(request, 'geekshop/contact.html')
