from django.contrib.auth.models import UserManager


class AccountsUserManager(UserManager):
    """
    Manager for User model
    """
    def verified(self):
        return self.filter(verified=True)
