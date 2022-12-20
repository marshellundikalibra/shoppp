from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Category, Product, ProductImage
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer
from rest_framework.views import APIView


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


from rest_framework import generics 
from .models import Category, Product, ProductImage

class CategoryListView(generics.ListAPIView):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer

class ProductListView(generics.ListAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer


class ProductView(generics.ListCreateAPIView):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

class ProductdetailView(generics.RetrieveUpdateAPIView):#detail
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

class ProductUpdateView(generics.UpdateAPIView):#put, patch
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

class ProductDeleteView(generics.DestroyAPIView):#delete
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
  
class PostImageView(generics.ListAPIView):
    queryset=ProductImage.objects.all()
    serializer_class=ProductImageSerializer

    def get_serializer_context(self):#photo from serializers 
        return {'request':self.request}


