import random
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP

def generate_and_send_otp(user):
    # Генерируем 6-значный код
    code = f"{random.randint(0, 999999):06d}"
    # Сохраняем
    OTP.objects.create(user=user, code=code)
    # Отправляем по email
    send_mail(
        subject='Ваш код подтверждения',
        message=f'Ваш код для входа: {code}',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )