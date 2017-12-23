from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Team(models.Model):
    name = models.CharField(_('name'), max_length=150)

    class Meta:
        ordering = ['name']
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')

    def __unicode__(self):
        return f"{self.name}"


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email', 'password']

    email = models.EmailField(_('email address'), blank=True, primary_key=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    verified = models.BooleanField(_('verified'), default=False)
    team = models.ForeignKey(Team, related_name='members')

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __unicode__(self):
        return f"{self.first_name} {self.last_name}"
