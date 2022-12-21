from rest_framework import serializers
from .models import MyUser
# from .utils import send_activation_code 
from django.contrib.auth import authenticate


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



# from .models import MyUser


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

    def create(self, validated_data):
        print('CREATING USER WITH DATA:', validated_data)
        return MyUser.objects.create_user(**validated_data)



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


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label=("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            if not user:
                message= ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(message, code='authorization')
        else:
            message = ('Must include "username" and "password".')
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs
"====================================================================================="


# class ForgotSerializer(serializers.Serializer):
#     email = serializers.EmailField()

#     def validate(self, attrs):
#         email = attrs.get('email')
#         try:
#             User.objects.get(email=email)
#         except User.DoesNotExist:
#             raise serializers.ValidationError('Such email does not found')
#         return attrs
    
#     def save(self):
#         data = self.validated_data
#         user = User.objects.get(**data)
#         user.set_activation_code()
#         user.password_confirm()

# class ChangePasswordSerializer(serializers.Serializer):
#     model = User

#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(
#         required=True, min_length=8, write_only=True
#     )