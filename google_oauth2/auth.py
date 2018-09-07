from django.contrib.auth import get_user_model

User = get_user_model()


def get_or_create_user(user_details):
    try:
        user = User.objects.get(email=user_details['user']['email'])
    except User.DoesNotExist:
        user = User.objects.create_user(**user_details['user'])
        # Handle integrity error
    return user
