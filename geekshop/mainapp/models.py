from django.db import models


class ProductCategory(models.Model):
    name = models.CharField(verbose_name='имя', max_length=64, unique=True)
    description = models.TextField(verbose_name='описание', blank=True)
    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        # return f'{self.name}'
        return f'{self.id} - {self.name}'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    name = models.CharField(
        verbose_name='имя продукта',
        max_length=128,
    )
    image = models.ImageField(
        upload_to='products_images',
        blank=True
    )
    short_descript = models.CharField(
        verbose_name='краткое описание',
        max_length=60,
        blank=True
    )
    description = models.TextField(
        verbose_name='описание',
        blank=True
    )
    price = models.DecimalField(
        verbose_name='цена',
        max_digits=8,
        decimal_places=2,
        default=0
    )
    quantity = models.PositiveIntegerField(
        verbose_name='количество',
        default=0
    )
    is_active = models.BooleanField(
        verbose_name='активен',
        default=True
    )

    def __str__(self):
        return f'{self.pk} - {self.category.name}'

    @staticmethod
    def get_items():
        return Product.objects.filter(is_active=True).order_by('category', 'name')


# class Productcategory(models.Model):
#     name = models.CharField(unique=True, max_length=64)
#     description = models.TextField()
#
#     class Meta:
#         managed = False
#         db_table = 'mainapp_productcategory'
# class Product(models.Model):
#     name = models.CharField(max_length=128)
#     image = models.CharField(max_length=100)
#     short_descript = models.CharField(max_length=60)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
#     category = models.ForeignKey('MainappProductcategory', models.DO_NOTHING)
#     quantity = models.PositiveIntegerField()
#
#     class Meta:
#         managed = False
#         db_table = 'mainapp_product'
