from django.db import models

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from posts.models import Post


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    commented_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commented_by')
    body = models.CharField(_('body'), max_length=255)
    pub_time = models.DateTimeField(_('publication time'), auto_now_add=True)

    class Meta:
        db_table = 'comments'
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class PostLike(models.Model):
    like = models.BooleanField(_('like'), default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like_post')
    liked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='liked_by')

    class Meta:
        db_table = 'likes'
        verbose_name = _('like')
        verbose_name_plural = _('likes')
