import datetime
import string
import random

from django.db.models import ObjectDoesNotExist
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

# from .utils import send_otp_email


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('You have not provided e-mail address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)

    def exist(self, email):
        try:
            self.get(email=email)
        except ObjectDoesNotExist:
            return None
        return True


class User(AbstractBaseUser):
    email = models.EmailField(blank=False, max_length=30, unique=True)
    # name = models.CharField(max_length=225, blank=True, default='')

    otp = models.CharField(max_length=6, default='')
    otp_exparation = models.DateTimeField(default=datetime.datetime.now())

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email.split('@')[0]

    def generate_otp(self, length=6):
        characters = string.digits
        otp = ''.join(random.choice(characters) for _ in range(length))
        self.otp = otp
        self.otp_exparation = datetime.datetime.now() + datetime.timedelta(minutes=10)
        self.save()
        return otp

    def checkout_otp(self, otp):
        if self.otp == otp and timezone.now() < self.otp_exparation:
            return True
        return False
