import random
import string

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.mail import send_mail

from accounts import managers


class Team(models.Model):
    """
    Team model is collection of User models.
    """
    name = models.CharField(_('name'), max_length=150)

    class Meta:
        ordering = ['name']
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser):
    """
    User model used for as main Authentication Model
    """

    objects = managers.AccountsUserManager()

    email = models.EmailField(_('email address'), blank=True, primary_key=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    verified = models.BooleanField(_('verified'), default=False)
    team = models.ForeignKey(Team, related_name='members', null=True)
    username = models.CharField(_('username'), max_length=150, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password', ]

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @staticmethod
    def generate_random_password(length=10):
        """
        :param: length: Length of password
        :return: Randomly generated password with [a-Z0-9] symbols
        """
        return ''.join(
            random.choices(
                string.ascii_uppercase + string.ascii_lowercase + string.digits,
                k=length)
        )

    def set_verified(self):
        """
        Set user as verified
        """
        self.verified = True
        self.save(update_fields=['verified', ])

    def send_mail(self, message, subject):
        """
        :param message:
        :param subject:
        :return: Status of sending mail
        """
        return send_mail(
            subject,
            message,
            # TODO: CHANGE TO REAL email
            'super_project@deee.de',
            [self.email],
            fail_silently=False,
        )

    def send_verification_mail(self, link):
        """
        :param link: Verification absolute url (type str)
        :return: status of sending mail. (type int)
        """
        message = f"Click this link {link}"
        return self.send_mail(message, subject='Verify your email')

    def reset_password(self):
        """
        Set new random generated password.
        """
        new_pwd = self.generate_random_password()
        message = _(f"Here you are, new password {new_pwd}")
        self.send_mail(message, subject='New password')
        self.set_password(new_pwd)
        self.save(update_fields=['password'])

    def send_invite_to_team(self, link):
        """
        :param link: Absolute url with invite to team (type str)
        :return: status of sending mail (type int)
        """
        message = _(
            f"Please, join our team {self.team.name}. Click this link {link}"
        )
        return self.send_mail(message, subject='Join Team')
