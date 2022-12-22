# from rest_framework import generics
# from .models import Order, Delivery
# from .serializers import OrderSerializer, DeliverySerializer


# class OrderListCreateView(generics.ListCreateAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer

#     def perform_create(self, serializer):
#         user = self.request.user
#         summa = 0
#         for item in user.cart.cart_items.all():
#             product_item = item.product_item
#             summa += product_item.price * item.amount
#             product_item.quantity -= item.amount
#             product_item.save()
#             item.delete()
            
#         serializer.save(
#             user=user,
#             cart=user.cart,
#             total=summa
#         )
            


# class OrderDetailView(generics.RetrieveAPIView):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer



# class DeliveryDetailView(generics.RetrieveAPIView):
#     queryset = Delivery.objects.all()
#     serializer_class = DeliverySerializer