import random
import string
from django.core.mail import send_mail
from django.conf import settings

def generate_otp(length=6):
    """Generates a numeric OTP of given length."""
    return ''.join(random.choices(string.digits, k=length))

def send_otp_email(email, otp):
    """Sends the OTP to the specified email."""
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}. It is valid for 10 minutes.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    try:
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_registration_email(email, username):
    """Sends a welcome email to the newly registered user."""
    subject = 'Welcome to ShoeStore!'
    message = f'Hi {username},\n\nThank you for registering at ShoeStore. We are excited to have you with us!\n\nBest Regards,\nThe ShoeStore Team'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    
    try:
        send_mail(subject, message, email_from, recipient_list)
        return True
    except Exception as e:
        print(f"Error sending registration email: {e}")
        return False
