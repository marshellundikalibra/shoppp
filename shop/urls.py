"""shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from product.views import CategoryListView, ProductViewSet, CommentViewSet, RatingViewSet, FavoriteViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('products',ProductViewSet )
router.register('comments', CommentViewSet)
# router.register('likes', LikeViewSet)
router.register('rating', RatingViewSet)
router.register('favorite', FavoriteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('product.urls')),
    path('api/account/', include('rest_framework.urls')),
    # path('v1/api/', include('product.urls')),
    path('v1/api/categories/', CategoryListView.as_view()),
    path('v1/api/account/', include('account.urls')),
    path('v1/api/',include(router.urls)),
    path('api-auth/', include('drf_social_oauth2.urls',namespace='drf')),
    # path('basket/', include('basket.urls')),
]
