import django
from django.db import models
from django.contrib.auth.models import AbstractUser

class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_ava', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст')
    # username = models.CharField(verbose_name='ник', blank=False, max_length=25, unique=True)
    # first_name = models.CharField(verbose_name='имя', blank=True, max_length=15)
    # password01 = models.CharField(verbose_name='пароль', blank=False, max_length=50)
    # password02 = models.CharField(verbose_name='пароль', blank=False, max_length=50)
    # mail = models.CharField(verbose_name='почта', max_length=30)

