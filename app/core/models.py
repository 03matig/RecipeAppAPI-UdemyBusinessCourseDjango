"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """ Manager for users. """

    def create_user(self, email, password=None, **extra_fields):
        """ Creates, saves and returns a new user. """
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)  # BaseUserManager should normalize the email.
        user.set_password(password)  # Can be excluded if you wan't to create an unusable user for testing.
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """ Creates super user"""
        if not email:
            raise ValueError('User must ahve an email address.')

        user = self.model(email=self.normalize_email(email))

        if not password:
            raise ValueError('User must have a password.')
        else:
            user.set_password(password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system. """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
