from django.contrib.auth import get_user_model
from django.test import TestCase

from mock import patch

from ..backends import GoogleOAuth2Backend
from .fixtures import user_details

User = get_user_model()


class SkipAuthentication(TestCase):
    def setUp(self):
        self.user_details = user_details()
        self.backend = GoogleOAuth2Backend()
        self.backend_name = 'google-oauth2'

    def test_return_None_if_no_backend_is_passed(self):
        user = self.backend.authenticate(user_details=self.user_details)
        self.assertIsNone(user)

    def test_return_None_if_backend_is_not_google_oauth2(self):
        user = self.backend.authenticate(backend='facebook-oauth2', user_details=self.user_details)
        self.assertIsNone(user)

    def test_return_None_if_no_user_details_are_passed(self):
        user = self.backend.authenticate(backend=self.backend_name)
        self.assertIsNone(user)


class AuthenticateUser(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='test'
        )
        self.user_details = user_details()
        self.backend_name = 'google-oauth2'
        self.backend = GoogleOAuth2Backend()

    @patch('google_oauth2.backends.get_or_create_user')
    def test_return_user(self, get_or_create_user_stub):
        get_or_create_user_stub.return_value = self.user
        user = self.backend.authenticate(
            backend=self.backend_name,
            user_details=self.user_details
        )
        self.assertEqual(self.user, user)
