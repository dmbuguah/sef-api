from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from sef.common.models import AbstractBase


class CustomUserManager(BaseUserManager):
    """
    A custom user manager for nugget
    """

    def create_user(self, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            **extra_fields
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBase, AbstractBaseUser):
    """
    A custom user model.
    """
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    email = models.EmailField(verbose_name='email address',
                              max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=150)
    phone_number = models.CharField(max_length=50)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_admin = models.BooleanField(default=False)
    objects = CustomUserManager()

    _search_fields = ('first_name', 'last_name', 'email', 'phone_number',)

    @property
    def full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email
