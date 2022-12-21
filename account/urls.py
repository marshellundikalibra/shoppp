from django.urls import path
from .views import *

urlpatterns=[
    path('register/',RegisterView.as_view()),
    path('activate/<str:activation_code>/', activate),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]