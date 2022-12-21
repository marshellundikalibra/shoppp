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

