from celery import shared_task
from .models import Todo
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

@shared_task
def send_mail_task():
    time_limit = timezone.now()+ timedelta(days=1)
    due = Todo.objects.filter(~Q(status="Completed"), due_date = time_limit)
    
    for i in due:
        user_email = i.user.email
        subject = f'Reminder, your task: {i.task} is due soon!'
        message = f'Dear User,\n\nYour task {i.task} is due on {i.due_date}. Please complete it as soon as possible.\n\nThankyou'
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)
    
    print("Email sent!") 
    
@shared_task
def hello_mail(email):
    send_mail(
        'Hello', 
        'Hello World', 
        settings.EMAIL_HOST_USER, 
        [email], 
        fail_silently=False,
        )
    return "Message Sent!"