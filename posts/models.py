from django.db import models

from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=255)
    body = models.TextField(_('body'))
    image = models.ImageField(width_field=100, height_field=100, blank=True)

    class Meta:
        db_table = 'posts'
        verbose_name = _('post')
        verbose_name_plural = _('posts')


