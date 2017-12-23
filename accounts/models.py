from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.core.mail import send_mail
from rest_framework.reverse import reverse

from core.utils import generate_hash


class Team(models.Model):
    """
    Team model is collection of User models.
    """
    name = models.CharField(_('name'), max_length=150)

    class Meta:
        ordering = ['name']
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')

    def __unicode__(self):
        return f"{self.name}"


class User(AbstractUser):
    """
    User model used for as main Authentication Model
    """
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

    def __unicode__(self):
        return f"{self.first_name} {self.last_name}"

    def set_verified(self):
        """
        Set user as verified
        """
        self.verified = True
        self.save(update_fields=['verified', ])

    def send_verification_mail(self):
        link = reverse("accounts-user-verify", kwargs={"email": generate_hash(self.email)})
        message = f"Click this link {link}"
        send_mail(
            'Verify your email! ',
            message,
            'org@de.com',
            [self.email],
            fail_silently=False,
        )
