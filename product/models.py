

from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, primary_key=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    def __str__(self):
        return self.title


LABEL_CHOICES = (
    ('new', 'Новинка'),
    ('bestseller', 'Хит продаж'),
    ('ordinary', 'Обычный')
)


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    label = models.CharField(max_length=10, choices=LABEL_CHOICES)
    
   

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')
    order = models.IntegerField()










# from django.db import models


# class Category(models.Model):
#     title = models.CharField(max_length=100)

#     def __str__(self):
#         return self.title


# class Product(models.Model):
#     category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     price = models.DecimalField(max_digits=10, decimal_places=2) # 9999999999.99
#     # quantity = models.IntegerField()
#     description = models.TextField()
#     status = models.CharField(max_length=15, choices=[('есть в наличии', 'in stock'), ('нет в наличии', 'out of stock'), ('ожидается', 'pending')])
#     image = models.ImageField(upload_to='images', null=True)

#     def __str__(self):
#         return f'[{self.category}] -> {self.title}'
