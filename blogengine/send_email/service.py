from django.core.mail import send_mail

from blogengine.settings import EMAIL_HOST_USER


def send(user_mail):
    send_mail(
        'Это тестовая безобидная рассылочка',
        'а до обновлений в блоге ещё дожить надо.\nХорошего дня)',
        EMAIL_HOST_USER,
        [user_mail],
        fail_silently=False,
    )