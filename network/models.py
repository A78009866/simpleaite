from django.contrib.auth.models import AbstractUser
from django.db import models
import json


class User(AbstractUser):
    following = models.ManyToManyField("Follower",symmetrical=False, related_name="followers")
    followed_by = models.ManyToManyField("Follower", symmetrical=False, related_name="following")
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "followers": len(list(self.followers.all())),
            "following": len(list(self.following.all()))
        }

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField("Like", symmetrical=False, related_name="liked_post")
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p")
        }

    def __str__(self):
        return "{'id': %s, 'user': %s, 'body': %s, 'timestamp': %s, 'likes': %s}" % (self.id, self.user.username, self.body, self.timestamp.strftime("%b %-d %Y, %-I:%M %p"), self.likes)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes", null=True)
    
    def __str__(self):
        return "{'user': %s, 'post': %s}" % (self.user, self.post)

class Follower(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE, related_name="followee", null=True)
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers", null=True)