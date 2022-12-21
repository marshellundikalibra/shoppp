# from django.db import models
# from apps.authentication.models import User
# from apps.products.models import Product


# class CartManger(models.Manager):
#     def get_or_new(self, request):
#         user = request.user
#         cart_id = request.session.get('cart_id', None)
#         if user is not None and user.is_authenticated:
#             if user.cart:
#                 cart_obj = request.user.cart
#             else:
#                 cart_obj = Cart.objects.get(pk=cart_id)
#                 cart_obj.user = user
#                 cart_obj.save()
#             return cart_obj
#         else:
#             cart_obj = Cart.objects.get_or_create(pk=cart_id)
#             cart_id = request.session['cart_id'] = cart_obj[0].id
#             return cart_obj[0]


# class Cart(models.Model):
#     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
#     objects = CartManger()


# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
#     product_item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_in_cart')
#     amount = models.PositiveIntegerField(default=1, blank=True)

#     def __str__(self):
#         return f"{self.cart.id} == cart item"

#Sultan


from django.db import models
from django.contrib.auth.models import User
from product.models import Products



class Cart(models.Model):
    session_key = models.CharField(max_length=999, blank=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_cost = models.PositiveIntegerField()
    

    def __str__(self):
        return str(self.id)

    @property
    def get_total(self):
        items = CartContent.objects.filter(cart=self.id)
        total = 0
        for item in items:
            total += item.product.price * item.qty
        return total

    @property
    def get_cart_content(self):
        return CartContent.objects.filter(cart=self.id)


class CartContent(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(null=True)