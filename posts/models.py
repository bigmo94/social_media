from django.db import models

from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField(_('body'), blank=True, null=True)
    pub_date = models.DateField(_('publication date'), auto_now_add=True)
    image = models.ImageField(upload_to='post_image', blank=True, null=True)

    class Meta:
        db_table = 'posts'
        verbose_name = _('post')
        verbose_name_plural = _('posts')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body = models.CharField(_('body'), max_length=255)
    pub_time = models.DateTimeField(_('publication time'), auto_now_add=True)

    class Meta:
        db_table = 'comments'
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')

    class Meta:
        db_table = 'likes'
        verbose_name = _('like')
        verbose_name_plural = _('likes')
