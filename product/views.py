from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, action
from .models import Category, Product, ProductImage
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, ProductImageSerializer
from rest_framework.views import APIView
from django.db.models import Q
from .models import *
from rest_framework.mixins import UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from django.utils import timezone
from datetime import timedelta


User = get_user_model()
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
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsAuthorPermission
from .serializers import *
from rest_framework.pagination import PageNumberPagination


class MyPaginationClass(PageNumberPagination):
    page_size=5
    def get_paginated_response(self, data):
        # print(data[0])
        for i in range(self.page.size):
            text=data[i]['text']
            data[i]['text']=text[:10]+'....'
            # print(data[1]['text'])
        return super().get_paginated_response(data)

class PermissionMixin:
    def get_permissions(self):#метод он встроенный
        print(self.action)#отправляет методы которыми были отправлены запросы
        if self.action == 'create':
            permissions = [IsAuthenticated, ]
        elif self.action in ['update', 'partial_update', 'destroy']:#put, patch. delete
            permissions = [IsAuthorPermission, ]#тип только автор может удалить
        else:
            permissions = []#и тогда он будет использовать только i
        return [permission() for permission in permissions]



class CategoryListView(generics.ListAPIView):#setting urls
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[AllowAny, ]
    pagination_class = MyPaginationClass



    

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
    permission_classes=[AllowAny, ]
    pagination_class=MyPaginationClass


    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(detail=False, methods=['get'])
    def my_products(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializers =ProductSerializer(queryset, many=True,
                                       context={'request': request})
        return Response(serializers.data, 200)

    #фильтрация продукты которые были опубкликованы не позже неделю назад или день
    # http://127.0.0.1:8000/v1/api/products/?week=1
    def get_queryset(self):
        queryset=super().get_queryset()
        weeks_count=int(self.request.query_params.get('days', 0))#query-params return dict
        if weeks_count>0:
            start_data=timezone.now()-timedelta(days=weeks_count)
            queryset=queryset.filter(created_at__gte=start_data)#фильтрация по  полю created_at
        return queryset

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


# class CommentViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [IsAuthenticated, IsAuthor]

class CommentViewSet(PermissionMixin, ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


# class LikeViewSet(PermissionMixin, ModelViewSet):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer
#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=['get'])
#     def my_likes(self, request, pk=None):
#         queryset = self.get_queryset()
#         queryset = queryset.filter(author=request.user)
#         serializers = LikeSerializer(queryset, many=True,
#                                          context={'request': request})
#         return Response(serializers.data, 200)

#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['action'] = self.action
#         return context


class RatingViewSet(PermissionMixin, ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def my_ratings(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializers = RatingSerializer(queryset, many=True,
                                         context={'request': request})
        return Response(serializers.data, 200)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context


class FavoriteViewSet(PermissionMixin, ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['action'] = self.action
        return context

    @action(detail=False, methods=['get'])
    def my_favorites(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializers = FavoriteSerializer(queryset, many=True,
                                         context={'request': request})
        return Response(serializers.data, 200)

class CreateLikeAPIView(APIView):
    # permission_classes = [IsAuthorOrReadOnly]
    # @swagger_auto_schema(request_body=LikeSerialzier())
    def post(self, request):
        print(request.data)
        user = request.user
        ser = LikeSerialzier(data=request.data, context={'request':request})
        ser.is_valid(raise_exception=True)
        l_id = request.data.get("product")

        if Like.objects.filter(product_id=l_id,author=user).exists():
            Like.objects.filter(product_id=l_id,author=user).delete()
        else:
            Like.objects.create(product_id=l_id,author=user)
        return Response(status=201)

# @api_view(['POST'])
# def toggle_like(request):
#     product_id = request.data.get("product")
#     email = request.data.get("email")
#     post = get_object_or_404(Product, id=product_id)
#     print(post)
#     email = get_object_or_404(User, email=email)
    
#     # if Like.objects.filter(product=post, author=email).exists():
#     #     # если был лайк
#     #     Like.objects.filter(product=post, author=email).delete()
#     #     # удаляем
#     # else:
#     #     # если лайка нет
#     #     Like.objects.create(product=post, author=email)
#         # создаем
#     return Response(status=201)