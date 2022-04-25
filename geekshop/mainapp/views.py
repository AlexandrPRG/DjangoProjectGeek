from django.shortcuts import render

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
}

def products(request):
    return render(request, 'mainapp/products.html', context=context)
