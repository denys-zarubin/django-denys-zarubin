from unittest import mock

from django.test import TestCase

from accounts.models import User
from tests.factories import UserFactory


class UserTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()

    def test_generate_random_password(self):
        res = self.user.generate_random_password()
        self.assertIsNotNone(res)

    def test_set_verified(self):
        self.assertFalse(self.user.verified)
        self.user.set_verified()
        self.assertTrue(self.user.verified)

    def test_send_mail(self):
        with mock.patch('django.core.mail.message.EmailMessage.send') as mm:
            self.user.send_mail('test', 'test')
            mm.assert_called()

    def test_send_verification_mail(self):
        with mock.patch.object(User, 'send_mail') as mm:
            self.user.send_verification_mail('http://google.com/')
            mm.assert_called_once_with('Click this link http://google.com/',
                                       subject='Verify your email')

    def test_reset_password(self):
        with mock.patch.object(User, 'send_mail') as mm:
            with mock.patch.object(User, 'generate_random_password',
                                   return_value='123'):
                self.user.reset_password()
                mm.assert_called_once_with('Here you are, new password 123',
                                           subject='New password')

    def test_send_invite_to_team(self):
        with mock.patch.object(User, 'send_mail') as mm:
            self.user.send_invite_to_team('http://google.com/')
            mm.assert_called_once_with(
                'Please, join our team Team 002.'
                ' Click this link http://google.com/',
                subject='Join Team')
