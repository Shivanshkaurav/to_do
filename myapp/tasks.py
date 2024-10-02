from celery import shared_task
from .models import Todo
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# @shared_task
# def send_mail_task():
#     time_limit = timezone.now()+ timedelta(days=4)
#     due = Todo.objects.filter(~Q(status="Completed"), due_date = time_limit)
    
#     for i in due:
#         user_email = i.user.email
#         subject = f'Reminder, {i.task} is due soon!'
#         message = f'Dear *{i.user}*,\n\nYour task, *{i.task}* is due on *{i.due_date}*. Please complete it as soon as possible.\n\n*Thankyou*'
#         send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email], fail_silently=False)
    
#     return "Email sent"


@shared_task
def send_mail_task():
    time_limit = timezone.now() + timedelta(days=4)
    due = Todo.objects.filter(~Q(status="Completed"), due_date=time_limit)

    for i in due:
        user_email = i.user.email
        subject = f'Your Task is Due Soon!'

        # Render the HTML template
        html_content = render_to_string('email_reminder.html', {
            'user': i.user,
            'task': i.task,
            'due_date': i.due_date,
        })
        
        # Optionally create a plain text version
        text_content = strip_tags(html_content)  # Removes HTML tags for plain text
        
        # Create email
        email = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [user_email])
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)

    return "Emails sent"