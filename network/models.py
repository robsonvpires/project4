from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    followers = models.ManyToManyField("self", related_name="following", blank=True, symmetrical=False)

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    body = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField("User", related_name="likes", blank=True)

    def getLikes(self):
        return [user.username for user in self.likes.all()]

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp,
            "likes": self.getLikes()
        }

    def __str__(self):
        return f"Posted by {self.user}"