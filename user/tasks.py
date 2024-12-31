from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email(email, code):
    send_mail(
        'Tasdiqlash kodi',
        f'Sizning tasdiqlash kodingiz: {code}',
        'admin@example.com',
        [email],
        fail_silently=False,
    )
