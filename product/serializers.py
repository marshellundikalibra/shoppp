from rest_framework import serializers
from .models import Category, Product, ProductImage
from .models import *
from decimal import Decimal
from django.db.models import Avg

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

        #сделать даже не зарегистрированный пользователь может просматривать
        
# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Product
#         fields=('id','title', 'description', 'category', 'price', 'discount_price','label')

#     def to_representation(self, instance):
#         rep=super().to_representation(instance)#instance обьект поста
#         rep['images']=ProductImageSerializer(instance.images.all(),many=True, context=self.context).data
#         return rep






class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id',  'title', 'description','category', 'price', 'discount_price', 'color', 'label',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['category'] = CategorySerializer(instance.category).data
        representation['images'] = ProductImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True, context=self.context).data
        representation['likes'] = instance.likes.count()

        rates = Rating.objects.filter(hostel=instance)
        if not rates:
            representation['rating'] = 'null'
        else:
            sum = 0
            for i in rates:
                sum = sum + i.rating
            representation['rating'] = Decimal(sum) / Decimal(Rating.objects.filter(hostel=instance).count())

        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        product= Product.objects.create(**validated_data)
        return 

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImage
        fields='__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url=obj.image.url
            request=self.context.get('request')

            if request is not None:
                url=request.build_absolute_uri(url)
        else:
            url=''
        return url

    def to_representation(self, instance):
        representation=super().to_representation(instance)
        representation['image']=self._get_image_url(instance)
        return representation
        '================================================================' 
'=========================================================================='


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        comment = Comment.objects.create(author=request.user, **validated_data)
        return comment


class LikeSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.email')

    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        likes, obj = Like.objects.update_or_create(author=request.user, **validated_data)
        return likes


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        rating, obj = Rating.objects.update_or_create(author=request.user, **validated_data)
        return rating


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
#тор тот кто является залогиненым all create
    def create(self, validated_data):
        request = self.context.get('request')#контекс в виевшке №в сериалайзере нету доступа к request #request нужен для того чтобы вытащить юзера
        favorite, obj = Favorite.objects.update_or_create(author=request.user, **validated_data)
        return favorite
    