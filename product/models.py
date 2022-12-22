
from account.models import MyUser

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

COLOR_CHOICES=(
    ('blue', 'Голубой'),
    ('grey', 'Серебристый'),
    ('gold', 'золотой'),
    ('graphite', 'графитовый'),
    ('white', 'Белый'),
    ('black','Черный')
)


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    color=models.CharField(max_length=20,null=True, choices=COLOR_CHOICES)
    label = models.CharField(max_length=10, choices=LABEL_CHOICES)
    # image = models.ImageField(upload_to='products', blank=True, null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    
   



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products', blank=True, null=True)
    # order = models.IntegerField()





class Comment(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('created',)


class Like(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='likes')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes')
    likes = models.BooleanField(default=False)

    def __str__(self):
        return self.likes


class Rating(models.Model):
    author = models.ForeignKey(MyUser, default='', on_delete=models.CASCADE, related_name='rating')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating')
    rating = models.SmallIntegerField()

    class Meta:
        ordering = ['-rating']

    def __str__(self):
        return f'{self.rating}'


class Favorite(models.Model):
    author = models.ForeignKey(MyUser, default='', on_delete=models.CASCADE, related_name='favorite')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorite')
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return self.favorite


















