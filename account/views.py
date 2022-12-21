from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authtoken.views import  ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token 
#Todo register view

class RegisterView(APIView):
    def post(self, request):
        data=request.data#у requets est attribute data здесь храняться все данные к-ые ввел пользоваьель №храниться словарь 
        #это дата который ввел пользователь попадает в serilaizers to validated_data
        serializer=RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):#raise_exception=True если все ненормально то нам будет генерироваться ошибка
            serializer.save()# сохрани данные который ввел пользователь 
            return Response('Successfully signed up!', status=status.HTTP_201_CREATED)

#to do activate, login logout view
from django.shortcuts import redirect

class ActivateView(APIView):
    def get(self, request, activation_code):
        User=get_user_model()
        user=get_object_or_404(User, activation_code=activation_code)#get_object_or_404 а вдруг этого юзера нет 52:04 тогда он будет генерировать 404 а если есть
        user.is_active=True
        user.activation_code='' #потому что он не может себя дважды активировать
        user.save()
        return redirect("http://127.0.0.1:8000/")
        # return Response("Your account successfully activated!",status=status.HTTP_200_OK)


#если такой юзер существует то ему дается токен


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

 
class LogoutView(APIView):
    permission_classes=[IsAuthenticated, ]
    
    def post(self, request):
        user=request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)
        
