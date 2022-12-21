from django.shortcuts import render
from rest_framework.decorators import api_view, action
from .models import Category, Product, ProductImage
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer
from rest_framework.views import APIView
from django.db.models import Q

from django.utils import timezone
from datetime import timedelta

# @api_view(['GET'])
# def categories(request):
#     if request.method=="GET":
#         categories=Category.objects.all()
#         serializer=CategorySerializer(categories, many=True)#который будет сериалтзовать филды которые мы передадим
#         return Response(serializer.data)


# class ProductListView(APIView):#данная виюшка будет возвращять списрк всех постов
#     def get(self, request):#возвращяет список продуктов
#         products=Product.objects.all()
#         serializer=ProductSerializer(products, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         product=request.data
#         serializer=ProductSerializer(data=product)
#         if serializer.is_valid(raise_exception=True):
#             product_saved=serializer.save()
#         return Response(serializer.data )


from rest_framework import generics , viewsets, status
from .models import Category, Product, ProductImage

class CategoryListView(generics.ListAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

# class ProductListView(generics.ListAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer


# class ProductView(generics.ListCreateAPIView):
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer

# class ProductdetailView(generics.RetrieveUpdateAPIView):#detail
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer

# class ProductUpdateView(generics.UpdateAPIView):#put, patch
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer

# class ProductDeleteView(generics.DestroyAPIView):#delete
#     queryset=Product.objects.all()
#     serializer_class=ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

    @action(detail=False, methods=['get'])#action работает nтолько с viewsets если на дженериках то поиск будет проводиться по методу get_queryset
    def search(self, request, pk=None):
        print(request.query_params)
        q=request.query_params.get('q')#query params заходит словарь q ключ а то что в поиске значение 
        queryset=self.get_queryset()#здесь находится  queryset=Product.objects.all() так как оно возвращяет все из модельки продукт нам нужно будет ее отфильтровать по этой q
        queryset=queryset.filter(Q(title__icontains=q) |
                                Q(description__icontains=q))#новый кверисет будет этому но отфильтрованный (фильтровать будем по названию и по тексту) in teat__icontains=q храниться тип поиск
        serializer=ProductSerializer(queryset, many=True, context={'request':request})#передаем отфильтрованный queryset
        return Response(serializer.data, status=status.HTTP_200_OK)
        # после product идет search

  
class ProductImageView(generics.ListAPIView):
    queryset=ProductImage.objects.all()
    serializer_class=ProductImageSerializer

    def get_serializer_context(self):#photo from serializers 
        return {'request':self.request}


