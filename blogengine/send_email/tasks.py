from django.core.mail import send_mail

from blogengine.celery import app
from blogengine.settings import EMAIL_HOST_USER
from .models import Contact


@app.task
def send_notification_email(user_email):
    send_mail(
        'Это тестовая безобидная рассылочка',
        'а до обновлений в блоге ещё дожить надо.\nХорошего дня)',
        EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,

    )

# TODO: rewrite with scheduling decorator
@app.task
def send_bullshit_email():
    for contact in Contact.objects.all():
        send_mail(
            'Это тестовая безобидная рассылочка',
            'будем дудосить (нет) тебя каждые несколько минут, но недолго..',
            EMAIL_HOST_USER,
            [contact.email],
            fail_silently=False,
        )