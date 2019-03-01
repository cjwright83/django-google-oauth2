from importlib import import_module

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def get_or_create_user(user_details):
    try:
        if hasattr(settings, 'GOOGLE_OAUTH2_USER_GET_FUNCTION'):
            user = _get_func(settings.GOOGLE_OAUTH2_USER_GET_FUNCTION)(user_details)
        else:
            user = User.objects.get(email=user_details.email)
    except User.DoesNotExist:
        if hasattr(settings, 'GOOGLE_OAUTH2_USER_CREATE_FUNCTION'):
            user = _get_func(settings.GOOGLE_OAUTH2_USER_CREATE_FUNCTION)(user_details)
        else:
            user = User.objects.create_user(**user_details.user)
        # Handle integrity error
    return user


def _get_func(s):
    m, f = s.rsplit('.', 1)
    mod = import_module(m)
    return getattr(mod, f)
