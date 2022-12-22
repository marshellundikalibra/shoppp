# from django.db import models

# from account.models import MyUser
# from product.models import Product

# class Order(models.Model):
#     product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='orders')
#     phone=models.CharField(max_length=13)
#     address=models.TextField()
#     city=models.CharField(max_length=100)
#     email=models.EmailField()

#     def __str__(self):
#         return f"{self.email}-{self.phone}"


# from django.db import models
# from django.contrib.auth.models import User
# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver

# from cart.models import Cart
# from .utils import randomString



# class Delivery(models.Model):
#     name = models.CharField(max_length=255, verbose_name="название", db_index=True)

#     class Meta:
#         verbose_name_plural = "Доставка"

#     def __str__(self):
#         return self.name
    


# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="пользователь", related_name="orders", null=True)
#     cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, verbose_name="корзина", null=True)
#     fname = models.CharField(verbose_name="имя", max_length=255)
#     lname = models.CharField(verbose_name="фамилия", max_length=255)
#     email = models.EmailField(verbose_name="email")
#     order_id = models.CharField(max_length=15, verbose_name="номер заказа", unique=True)
#     address = models.CharField(verbose_name="адрес", max_length=255)
#     delivery = models.ForeignKey(Delivery, on_delete=models.SET_NULL, verbose_name="Доставка", related_name='orders', null=True)
#     created = models.DateTimeField(auto_now_add=True)
#     paid = models.BooleanField(default=False, verbose_name="оплаченный")
#     total = models.DecimalField(max_digits=100, decimal_places=2, default=0, verbose_name="общий сумма", null=True)

#     class Meta:
#         ordering = ('-id',)
#         verbose_name_plural = "Заказы"

#     def __str__(self):
#         return f"order {self.order_id}"

    
# @receiver(pre_save, sender=Order)
# def pre_save_order_id(sender, instance, *args, **kwargs):
#     if not instance.order_id:
#         instance.order_id = randomString()

# class Rassrochka(models.Model):

