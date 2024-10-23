# sms_notifications.py
from twilio.rest import Client
from django.conf import settings

def send_payment_success_sms(user, amount):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    message = f"Dear {user.username}, your payment of {amount} was successful."
    
    client.messages.create(
        to=user.phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=message
    )

def send_payment_failure_sms(user, amount):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    message = f"Dear {user.username}, your payment of {amount} failed. Please try again."
    
    client.messages.create(
        to=user.phone_number,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=message
    )
