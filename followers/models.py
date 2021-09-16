from django.db import models

from django.conf import settings
from django.utils.translation import gettext_lazy as _


class UserFollowing(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="followers", on_delete=models.CASCADE)
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)

    class Meta:
        unique_together = ['user_id', 'following_user_id']
        db_table = 'user_followings'

    def __str__(self):
        return f'{self.user_id} follows {self.following_user_id}'
