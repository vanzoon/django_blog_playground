# import os
# import requests
# from celery import shared_task
# from django.core.mail import send_mail
#
# import blogengine.settings
# from blogengine.celery import app
# from blogengine.settings import EMAIL_HOST_USER
#
# # timezone = 'Europe/London'
#
#
# @app.task()
# def send_notification_email(user_email):
#     try:
#         send_mail(
#             'Это тестовая безобидная рассылочка',
#             'а до обновлений в блоге ещё дожить надо.\nХорошего дня)',
#             EMAIL_HOST_USER,
#             [user_email],
#             fail_silently=False,
#         )
#     except:
#         raise Exception("something bad happend")
#
# app.conf.beat_schedule = {
#     'send_email_at_every_6_am': {
#         'task': 'tasks.send_notification_email',
#         'schedule': crontab(hour=6, minute=0, day_of_week=1),
#         # 'args': (celedshka@gmail.com),
#     },
# }
