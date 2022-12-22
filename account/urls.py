from django.urls import path
from .views import *


urlpatterns=[
    path('register/',RegisterView.as_view()),
    path('activate/<str:activation_code>/', activate),
    path('login/', LoginSerializer.as_view()),
    path('logout/', LogoutView.as_view()),
    # path('delete/', ())

    # path('change_password/', ChangePasswordView.as_view()),
    # path('forgot_password/', ForgotPasswordView.as_view()),
]