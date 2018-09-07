from django.contrib.auth import get_user_model

from .auth import get_or_create_user

User = get_user_model()


class GoogleOAuth2Backend(object):
    def authenticate(self, *args, **kwargs):
        if ('backend' in kwargs and
                kwargs['backend'] == 'google-oauth2' and
                'user_details' in kwargs):
            return get_or_create_user(kwargs['user_details'])
        return None

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)
