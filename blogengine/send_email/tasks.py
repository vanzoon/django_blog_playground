from blogengine.celery import app
from .service import send


@app.task
def send_notification_email(user_email):
    send(user_email)
