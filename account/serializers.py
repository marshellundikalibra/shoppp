from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import MyUser
# from .utils import send_activation_code 
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenObtainPairView

User = get_user_model()

#TO DO serializer

# class RegisterSerializer(serializers.ModelSerializer):
#     password=serializers.CharField(min_length=6, write_only=True)
#     password_confirm=serializers.CharField(min_length=6, write_only=True)

#     class Meta:
#         model=MyUser
#         fields=('email','password', 'password_confirm')#пароли должны храниться в хэштрованном виде  из за этого все это мы не прописывали в модельках 

#     def validate(self, validated_data):#def validate=def clean #приходят виде словаря 
#         print(validated_data)
#         password=validated_data.get('password')
#         password_confirm=validated_data.get('password_confirm')
#         if password != password_confirm:
#             raise serializers.ValidationError('Passwords do not match ')#у сериалайзеров есть такая ошибка ValidationError
#         return validated_data #сли пароли совпадают




class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=4, required=True)

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'password_confirm')

    def validate(self, attrs):
        # attrs = {"email":"some@gmail.com", "password":"1234", "password_confirm":"1234"}
        pass1 = attrs.get("password")
        pass2 = attrs.pop("password_confirm")
        if pass1 != pass2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def validate_email(self, email):
        # email = "some@gmail.com"
        if MyUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User with this email already exists")
        return email

    # def create(self, validated_data):
    #     # validated_data = {"email":"some@gmail.com", "password":"1234", "password_confirm":"1234"}
    #     return MyUser.objects.create_user(**validated_data)

    # def create(self, validated_data):
    #     print('CREATING USER WITH DATA:', validated_data)
    #     return MyUser.objects.create_user(**validated_data)

    def save(self):
        data = self.validated_data
        user = User.objects.create_user(**data)
        user.set_activation_code()
        user.send_activation_code()

    #     #сделали после activation code from model
    # def create(self, validated_data):#будет создавать юзера надо переопределить потомучто сюда высылаем код активации
    #     #вызывается когда сохраням обьект 
    #     """This function is called when self.save()method is called """
    #     email=validated_data.get('email')
    #     password=validated_data.get('password')
    #     #вытащили email and password чтобы передать в create_user
    #     user=MyUser.objects.create_user(email=email,password=password)   #create_user from models и он принимает email and password 
    #     # from utils
    #     send_activation_code(email=user.email, activation_code=user.activation.code) #and from user мы можем обраттиться 
    #     return user
    # #     #обьект модельки MYUSER

#To DO login Serializer

class LoginSerializer(TokenObtainPairView):

    pass


class ForgotSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Such email does not found')
        return attrs
    
    def save(self):
        data = self.validated_data
        user = User.objects.get(**data)
        user.set_activation_code()
        user.password_confirm()

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(
        required=True, min_length=8, write_only=True
    )

# #CREATE
# class CreateNewPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     activation_code = serializers.CharField(max_length=40, required=True)
#     password = serializers.CharField(min_length=8, required=True)
#     password_confirmation = serializers.CharField(min_length=8, required=True)

#     def validate_email(self, email):
#         if not MyUser.objects.filter(email=email).exists():
#             raise serializers.ValidationError("Пользователь не найден)")
#         return email

#     def validate_activation_code(self, act_code):
#         if not MyUser.objects.filter(activation_code=act_code,
#                                      is_active=False).exists():
#             raise serializers.ValidationError('Неверный код активации')
#         return act_code

#     def validate(self, attrs):
#         password = attrs.get('password')
#         password_confirmation = attrs.pop('password_confirmation')
#         if password != password_confirmation:
#             raise serializers.ValidationError('Пароли не совпадают')
#         return attrs

#     def save(self, **kwargs):
#         data = self.validated_data
#         email = data.get('email')
#         activation_code = data.get('activation_code')
#         password = data.get('password')
#         try:
#             user = MyUser.objects.get(email=email, activation_code=activation_code, is_active=False)
#         except MyUser.DoesNotExist:
#             raise serializers.ValidationError("Пользователь не найден")
#         user.is_active = True
#         user.activation_code = ''
#         user.set_password(password)
#         user.save()
#         return 