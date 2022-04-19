from django.urls import path, include
from .views import index, contacts

urlpatterns = [
    # path('', index),
    path('contacts/', contacts),
    path('', include('mainapp.urls'))
]