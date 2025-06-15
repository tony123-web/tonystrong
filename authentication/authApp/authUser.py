from .models import Account

def authenticate_user(email, password):
    try:
        user=Account.objects.get(email=email)
        validate_user_password=user.check_password(password)
        if validate_user_password:
            return user
        return None
    except Account.DoesNotExist:
        return None