from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            email=self.normalize_email(email), username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staff_user(self, email, username, password):
        user = self.create_user(
            email,
            password=password, username=username)
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email,
            password=password, username=username)
        user.staff = True
        user.superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(_('username'), max_length=32, unique=True)
    email = models.EmailField(_('email'), max_length=64, unique=True)
    phone_number = PhoneNumberField(_('phone number'), unique=True, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    active = models.BooleanField(_('is active'), default=True)
    staff = models.BooleanField(_('is staff'), default=False)
    superuser = models.BooleanField(_('is superuser'), default=False)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_superuser(self):
        return self.superuser

    @property
    def is_active(self):
        return self.active


class Profile(models.Model):
    Male = 1
    Female = 2
    GENDER_CHOICES = (
        (Male, 'Male'),
        (Female, 'Female')
    )

    first_name = models.CharField(_('first name'), max_length=32)
    last_name = models.CharField(_('last name'), max_length=32)
    gender = models.IntegerField(_('gender'), choices=GENDER_CHOICES, blank=True)
    birth_date = models.DateField(_("birthday"), blank=True)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pic')
    bio = models.CharField(_('biography'), max_length=255, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
