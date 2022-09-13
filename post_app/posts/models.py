from django.conf import settings
from django.db import models


class Post(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
    )
    title = models.CharField(max_length=128)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="likes", through="PostLike"
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
