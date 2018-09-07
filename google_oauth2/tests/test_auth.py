from django.contrib.auth import get_user_model
from django.test import TestCase

from ..auth import get_or_create_user
from .fixtures import user_details

User = get_user_model()


class RetrieveExistingUser(TestCase):
    def test_return_existing_user_by_email(self):
        existing_user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='test',
        )
        retrieved_user = get_or_create_user(user_details())
        self.assertEqual(retrieved_user, existing_user)


class CreateNewUser(TestCase):
    def test_create_a_new_user(self):
        initial_user_count = User.objects.count()
        get_or_create_user(user_details())
        self.assertEqual(initial_user_count + 1, User.objects.count())

    def test_return_the_new_user(self):
        user = get_or_create_user(user_details())
        self.assertEqual(user, User.objects.last())


class GetExistingUser(TestCase):
    def test_(self):
        pass
