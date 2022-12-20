

from django.contrib import admin
from .models import Product, Category, ProductImage

class PostImageInline(admin.TabularInline):
    model=ProductImage
    max_num=6
    min_num=1


admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductImage)