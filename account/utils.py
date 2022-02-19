from django.core.mail import send_mail


def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/api/v1/account/activate/{activation_code}'
    message = f"""
        Спасибо, что зарегистрировались. 
        Пожалуйста, активируйте ваш аккаунт.
        Активационный код: {activation_url}"""

    send_mail(
        'Активируйте ваш аккаунт',
        message,
        'admin@admin.com',
        [email, ],
        fail_silently=False     # если будет ошибка, нам сгенерируется ошибка
    )