from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status 
from rest_framework.authtoken.views import  ObtainAuthToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token 


from rest_framework.generics import get_object_or_404, GenericAPIView, ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
#Todo register view




class RegisterView(APIView):
    def post(self, request):
        data=request.data#у requets est attribute data здесь храняться все данные к-ые ввел пользоваьель №храниться словарь 
        #это дата который ввел пользователь попадает в serilaizers to validated_data
        serializer=RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):#raise_exception=True если все ненормально то нам будет генерироваться ошибка
            serializer.save()# сохрани данные который ввел пользователь 
            return Response('Successfully signed up!', status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete(request, email):
    user = get_object_or_404(MyUser, email=email)
    if user.is_staff:
        return Response(status=403) # запрещаем
    user.delete()
    return Response('Your account successfully deleted', status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def activate(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = ''
    user.save()
    return redirect("http://127.0.0.1:8000/admin/")


#==============================================================================
# class ChangePasswordView(UpdateAPIView):
#     serializer_class = ChangePasswordSerializer
#     model = User
#     permission_classes = [IsAuthenticated, ] 

#     # @swagger_auto_schema(request_body=ChangePasswordSerializer)
#     def update(self, request, *args, **kwargs):
#         object = request.user
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             if not object.check_password(request.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

#             object.set_password(request.data.get("new_password"))
#             object.is_active = True
#             object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully'
#             }

#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#=================================================================================

#to do activate, login logout view
from django.shortcuts import redirect

# class ActivateView(APIView):
#     def get(self, request, activation_code):
#         User=get_user_model()
#         user=get_object_or_404(MyUser, activation_code=activation_code)#get_object_or_404 а вдруг этого юзера нет 52:04 тогда он будет генерировать 404 а если есть
#         user.is_active=True
#         user.activation_code='' #потому что он не может себя дважды активировать
#         user.save()
#         # return redirect("http://127.0.0.1:8000/")
#         return Response("Your account successfully activated!",status=status.HTTP_200_OK)


#если такой юзер существует то ему дается токен


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

 
class LogoutView(APIView):
    permission_classes=[IsAuthenticated, ]
    
    def post(self, request):
        user=request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logged out', status=status.HTTP_200_OK)
        
'================================================================'

# class ForgotPasswordView(APIView):
#     # @swagger_auto_schema(request_body=ForgotSerializer)

#     def post(self, request):
#         data = request.POST
#         serializer = ForgotSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             message = "Please, confirm your new password"
#             return Response(message)


# class NewPasswordView(APIView):
#     def get(self, request, activation_code):
#         user = get_object_or_404(User, activation_code=activation_code)
#         new_password = user.generate_activation_code()
#         user.set_password(new_password)
#         user.save()
        # return Response(f"Your new password is {new_password}")