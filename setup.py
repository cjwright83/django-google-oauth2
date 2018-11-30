from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    user_options = [("pytest-args=", "a", "Arguments to pass to pytest")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = ""

    def run_tests(self):
        import django
        from django.conf import settings

        import pytest

        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {'ENGINE': 'django.db.backends.sqlite3'}
            },
            INSTALLED_APPS=(
                'django.contrib.contenttypes',
                'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.staticfiles',
            ),
            USE_TZ=True
        )

        django.setup()
        return pytest.main(['--verbose'])


tests_require = [
    'Django>=1.11.16,<2',
    'mock>=2.0',
    'pytest>3,<4',
    'pytest-django>3,<4'
]

setup(
    name='django-google-oauth2',
    version='0.1',
    description='Views and helpers for interacting with Google APIs via OAuth2 in a Django app.',
    url='http://github.com/cjwright83y/django-google-oauth2/',
    author='Chris Wright',
    author_email='cjwright83y@gmail.com',
    license='MIT',
    packages=find_packages(
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"]
    ),
    zip_safe=False,
    install_requires=[
        'google-auth-oauthlib >= 0.2.0'
    ],
    cmdclass={'test': PyTest},
    tests_require=tests_require,
    extras_require=dict(
        test=tests_require
    )
)
