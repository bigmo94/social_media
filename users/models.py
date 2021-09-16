from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class Profile(AbstractUser):
    phone_number = PhoneNumberField(_('phone number'), unique=True, blank=True, null=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    Male = 1
    Female = 2
    GENDER_CHOICES = (
        (Male, 'Male'),
        (Female, 'Female')
    )

    gender = models.IntegerField(_('gender'), choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(_("birthday"), blank=True, null=True)
    profile_picture = models.ImageField(blank=True, upload_to='profile_pic', null=True)
    bio = models.CharField(_('biography'), max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'profiles'
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')

    def __str__(self):
        return self.username


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    body = models.TextField(_('body'))

    class Meta:
        db_table = 'messages'
        verbose_name = _('message')
        verbose_name_plural = _('messages')


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followings", on_delete=models.CASCADE)
    following = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)

    class Meta:
        db_table = 'follows'
