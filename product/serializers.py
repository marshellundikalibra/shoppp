from rest_framework import serializers

from .models import Category, Product, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=('id','title', 'description', 'category', 'price', 'discount_price','label')

    def to_representation(self, instance):
        representation=super().to_representation(instance)#instance обьект поста
        representation['images']=ProductImageSerializer(instance.images.all(),many=True, context=self.context).data
        
        return representation


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
        
    