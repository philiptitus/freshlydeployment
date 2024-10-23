from urllib import response
from django.conf import settings  # Import settings to access constants
from .models import Transaction
from .email_notifications import send_payment_success_email, send_payment_failure_email
from .sms_notifications import send_payment_success_sms, send_payment_failure_sms
import time
import logging

logger = logging.getLogger(__name__)

def lipa_na_mpesa_online(user, phone_number, amount, retries=None):
    # Use the retries value from settings if not passed explicitly
    retries = retries or settings.MAX_RETRIES
    
    transaction = Transaction.objects.create(
        user=user, 
        phone_number=phone_number, 
        amount=amount, 
        status='pending'
    )

    for attempt in range(retries):
        try:
            # (The rest of the payment logic remains the same...)

            if response.status_code == 200:
                result = response.json()
                if result.get('ResponseCode') == '0':
                    # Transaction successful
                    transaction.status = 'completed'
                    transaction.mpesa_receipt_number = result.get('MerchantRequestID')
                    transaction.save()
                    
                    # Notify the user via email and SMS
                    send_payment_success_email(user, amount)
                    send_payment_success_sms(user, amount)
                    
                    return transaction
                else:
                    raise Exception(result.get('errorMessage', 'Unknown Error'))

            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")

        except Exception as e:
            logger.error(f"Error during payment attempt {attempt+1}: {e}")
            transaction.error_message = str(e)

        if attempt < retries - 1:
            time.sleep(settings.RETRY_DELAY)

    # Mark transaction as failed
    transaction.status = 'failed'
    transaction.save()
    
    # Notify the user via email and SMS about the failure
    send_payment_failure_email(user, amount)
    send_payment_failure_sms(user, amount)

    return transaction
