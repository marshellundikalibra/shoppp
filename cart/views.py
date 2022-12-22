# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view

# from product.models import Product

# from .models import Cart, CartItem
# from .serializers import CartSerializer, CartItemSerializer


# class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Cart.objects.all()
#     serializer_class = CartSerializer

#     def retrieve(self, request):
#         queryset = Cart.objects.get_or_new(request)
#         serializer = CartSerializer(queryset, context={'request': request})
#         return Response(status=status.HTTP_200_OK, data=serializer.data)


# class CartItemDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer


# class CartItemView(generics.CreateAPIView):
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer

#     def post(self, request, *args, **kwargs):
#         cart = Cart.objects.get_or_new(request)
#         cartitems = cart.cart_items.all()
#         product_item = Product.objects.get(pk=request.data['product_item'])
#         for item in cartitems:
#             if item.product_item == product_item:
#                 return Response(data={'message': 'The product is already in the cart'}, status=status.HTTP_400_BAD_REQUEST)
#             if product_item.quantity == 0 or int(request.data['amount']) > product_item.quantity:
#                 return Response(data={'message': 'No enough quantity'}, status=status.HTTP_400_BAD_REQUEST)
#         return self.create(request, *args, **kwargs)

#     def perform_create(self, serializer):
#         cart = Cart.objects.get_or_new(self.request)
#         serializer.save(cart=cart)


# @api_view(['GET'])
# def session_get(request):
#     print(request.session.get('cart'))
#     return Response(data={"message": f"{request.session.get('cart')}"}, status=status.HTTP_200_OK)