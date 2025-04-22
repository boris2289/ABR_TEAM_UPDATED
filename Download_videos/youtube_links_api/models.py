from django.contrib.auth.models import User
from django.db import models
from django.conf import settings


class YouTubeLink(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True, null=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

class Comment(models.Model):
    youtube_link = models.ForeignKey(YouTubeLink, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.youtube_link.name}"

class Like(models.Model):
    youtube_link = models.ForeignKey(YouTubeLink,
                                     related_name='likes',
                                     on_delete=models.CASCADE)

    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Liked {self.youtube_link.name}"

class Category(models.Model):
    youtube_links = models.ManyToManyField(YouTubeLink,
                                           related_name="categories")
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
