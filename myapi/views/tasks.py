
from django.contrib.auth.models import User
import telegram_send
from celery import shared_task

@shared_task
def telegram_send_report(x):
    telegram_send.send(messages=[x,])
    return 'report Send Successfully'