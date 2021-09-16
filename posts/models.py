from django.db import models

from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='post_user')
    title = models.CharField(_('title'), max_length=100, blank=True)
    body = models.TextField(_('body'))
    image = models.ImageField(upload_to='post_image', width_field=100, height_field=100, blank=True)
    pub_date = models.DateField(_('publication date'), auto_now_add=True)

    class Meta:
        db_table = 'posts'
        verbose_name = _('post')
        verbose_name_plural = _('posts')
