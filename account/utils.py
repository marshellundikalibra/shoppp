#отправка кода активации
# from django.core.mail import send_mail

# def send_activation_code(email, activation_code):
#     activation_url=f"http://127.0.0.1:8000/v1/api/account/activate/{activation_code}"
#     message=f"""
#     Thank you for signing up.
#     Please, activate your account.
#     Activation Link: {activation_url}
#     """
#     send_mail(
#         'Activate your account',
#         message,
#         'test@test.com',#с какого эммейла будет приходить №..он не проверяет является ли еьайл настоящим
#         [email, ], #на какой email должен отправляться 
#         fail_silently=False #если при send activation code если что то сломается то нам сгенерируется определенная ошибка
#     )

# def send_activation_code(self ):
#         from django.core.mail import send_mail
#         self.create_activation_code()
#         activation_link=f"http://127.0.0.1:8000/v1/api/account/activate/{self.activation_code}"
#         message=f"Активируйте свой аккаунт, перейдя по ссылке\n{activation_link} "
#         send_mail("Activate account", message,'marshellundikalibra171005@gmail.com' ,recipient_list=[self.email], fail_silentlu=False)

        
