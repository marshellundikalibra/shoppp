from django.urls import path
from .views import CreateLikeAPIView


urlpatterns = [
    path('likefilms/', CreateLikeAPIView.as_view()),
]
# urlpatterns=[
#     # path('categories/', views.categories, name='categories-list'),
#     path('categories/', views.CategoryListView.as_view(), name='categories-list'),
#     path('products/', views.ProductView.as_view(), name='posts-list'),

#       # path('posts/', views.PostListView.as_view(), name='post-list'),
#     # path('posts/', views.PostView.as_view(), name='post-list'),
#     # path('post-create/', views.ProductCreateView.as_view(), name='product-create'),
#     path('products/<int:pk>/', views.ProductdetailView.as_view(), name='product-detail'),
#     path('products-update/<int:pk>/', views.ProductUpdateView.as_view()),
#     path('products-delete/<int:pk>/', views.ProductDeleteView.as_view()),
#     # path('posts-detail/<int:pk>/', views.PostImageView.as_view()),


# ]
