from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)#здесь потому что в базе данных должен храниться в хэшированном виде
        user.is_active = False #оно станет тру только тогда когда пользователь получит код активации перейдет по ссылке и активирует себя 
        # user.create_activation_code()
        user.save(using=self._db)#какую базу данных он будет использовать
        return user
    
    
    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        
        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)

        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        

        user.save(using=self._db)
        return user


class MyUser(AbstractUser):
    username=None
    email = models.EmailField(max_length=150, unique=True)
    # username = models.CharField(max_length=150)
    is_active=models.BooleanField(default=False)
    activation_code = models.CharField(max_length=50, blank=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self):
        return self.email

#create activation code 
# 20:30
    # def create_activation_code(self):
    #     import hashlib
    #     string=self.email+str(self.id)
    #     encode_string=string.encode()
    #     md5_object=hashlib.md5(encode_string)
    #     activation_code=md5_object.hexdigest()#чтобы он все это переварил и выдал что то непонятное
    #     self.activation_code=activation_code #self.activation_code -> из MyUser activation_code 
        
    # def send_activation_code(self ):
    #     from django.core.mail import send_mail
    #     self.create_activation_code()
    #     activation_link=f"http://127.0.0.1:8000/v1/api/account/activate/{self.activation_code}"
    #     message=f"Активируйте свой аккаунт, перейдя по ссылке\n{activation_link} "
    #     send_mail("Activate account", message,'wordreplaceword171005@gmail.com' ,recipient_list=[self.email])

    @staticmethod
    def generate_activation_code():
        from django.utils.crypto import get_random_string
        code = get_random_string(8)
        return code 

    def set_activation_code(self):
        code = self.generate_activation_code()
        if MyUser.objects.filter(activation_code=code).exists():
            self.set_activation_code()
        else:
            self.activation_code = code
            self.save()
    
    def send_activation_code(self ):
        from django.core.mail import send_mail
        self.generate_activation_code()
        self.set_activation_code()
        activation_link=f"http://127.0.0.1:8000/v1/api/account/activate/{self.activation_code}"
        message=f"Активируйте свой аккаунт, перейдя по ссылке\n{activation_link} "
        send_mail("Activate account", message,'wordreplaceword171005@gmail.com' ,recipient_list=[self.email])
