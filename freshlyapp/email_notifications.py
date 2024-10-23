#/email_notifications.py
from django.core.mail import send_mail
from django.conf import settings

def send_payment_success_email(user, amount):
    subject = 'Payment Successful'
    message = f"Dear {user.username}, your payment of {amount} has been successfully processed."
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def send_payment_failure_email(user, amount):
    subject = 'Payment Failed'
    message = f"Dear {user.username}, your payment of {amount} has failed. Please try again."

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
