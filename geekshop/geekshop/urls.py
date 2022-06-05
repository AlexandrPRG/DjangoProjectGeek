"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.contrib import admin
from django.urls import path, include

import geekshop.views

from .views import index, contacts
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.list import ListView


urlpatterns = \
    [
    path('admin/', admin.site.urls),
    # path('', index, name='index'),
    path('', geekshop.views.IndexTemplateView.as_view(), name='index'),
    path('contacts/', contacts, name='contacts'),

    path('auth/', include('authapp.urls', namespace='auth')),
    path('products/', include('mainapp.urls', namespace='products')),
    path('basket/', include('basketapp.urls', namespace='basket')),
    path('orders/', include('ordersapp.urls', namespace='orders')),
    path('admin_stuff/', include('adminapp.urls', namespace='admin_stuff')),

    path('', include('social_django.urls', namespace='social')),
    ]
if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
