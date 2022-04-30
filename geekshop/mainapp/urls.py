from django.urls import path
from .views import products

app.name = 'mainapp'
urlpatterns = [
    path('', products, name='index'),
]
