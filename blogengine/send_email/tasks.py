from celery.schedules import crontab
from django.core.mail import send_mail

from blogengine.celery import app
from blogengine.settings import EMAIL_HOST_USER
from .models import Contact

timezone = 'Europe/London'


@app.task
def send_notification_email(user_email):
    send_mail(
        'Это тестовая безобидная рассылочка',
        'а до обновлений в блоге ещё дожить надо.\nХорошего дня)',
        EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,

    )


@app.task(run_every=(crontab(minute='*/5')), name="send_bullshit_every_5_min")
def send_bullshit_email():
    for contact in Contact.objects.values('username', 'email'):
        send_mail(
            'Это тестовая безобидная рассылочка',
            'будем желать вам доброго дня каждые 5 минут',
            EMAIL_HOST_USER,
            [contact.email],
            fail_silently=False,
        )
