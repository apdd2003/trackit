# tasks.py

from celery import shared_task
from django.core.mail import send_mail
# from mysite import settings


@shared_task(bind=True)
def send_notification_mail(self, title):
    send_mail(
        f"Trackit V2.0 - A new post is submitted",
        f"A post - {title} is submitted and waiting for approval",
        "sayeem.shaikh@gmail.com",
        ["sayeem.shaikh@gmail.com"],

    )
    return "Done"
