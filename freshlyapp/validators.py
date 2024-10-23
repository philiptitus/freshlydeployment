from rest_framework.exceptions import ValidationError
import re
from django.contrib.auth import get_user_model


User = get_user_model()

def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValidationError("Invalid email format.")
    if User.objects.filter(email=email).exists():
        raise ValidationError("Email is already registered.")
    return email

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(char.isdigit() for char in password):
        raise ValidationError("Password must contain at least one numeral.")
    if not any(char.isalpha() for char in password):
        raise ValidationError("Password must contain at least one letter.")
    if not any(char in "!@#$%^&*()_+-=[]{};:'\"\\|,.<>/?`~" for char in password):
        raise ValidationError("Password must contain at least one special character.")
    return password

def custom_validation(data):
    # Ensure required fields are present
    if 'email' not in data or 'password' not in data:
        raise ValidationError("Email and password are required.")
    
    # Validate email
    validate_email(data['email'])
    
    # Validate password
    validate_password(data['password'])

    # Confirm password validation (if applicable)
    if 'confirm_password' in data and data['password'] != data['confirm_password']:
        raise ValidationError("Passwords do not match.")