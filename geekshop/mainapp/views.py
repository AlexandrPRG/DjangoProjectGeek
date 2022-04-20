from django.shortcuts import render


def products(request):
    print(request, 'mainapp/products.html')
    return render(request, 'mainapp/products.html')
