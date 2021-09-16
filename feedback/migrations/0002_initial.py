# Generated by Django 3.2.7 on 2021-09-16 06:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0001_initial'),
        ('feedback', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postlike',
            name='liked_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postlike',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like_post', to='posts.post'),
        ),
        migrations.AddField(
            model_name='comment',
            name='commented_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_post', to='posts.post'),
        ),
    ]
