

from django.contrib import admin
from .models import Product, Category, ProductImage

# class PostImageInline(admin.TabularInline):
#     model=ProductImage
#     max_num=6
#     min_num=1


# admin.site.register(Product)
# admin.site.register(Category)
# admin.site.register(ProductImage)


from django.contrib import admin

from .models import *

class ProductImageInline(admin.TabularInline):
    model=ProductImage
    max_num=1
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductImageInline, ]

admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(Comment)
# admin.site.register(LikeComment)

admin.site.register(Rating)
# admin.site.register(Favourite)