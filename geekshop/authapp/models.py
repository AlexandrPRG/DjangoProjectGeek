import django
from django.db import models
from django.contrib.auth.models import AbstractUser, User

class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users_ava', blank=True)
    age = models.PositiveIntegerField(verbose_name='возраст')

