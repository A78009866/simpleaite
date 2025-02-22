from django.contrib.auth.models import AbstractUser
from django.db import models
<<<<<<< HEAD

class User(AbstractUser):
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='network_user_groups',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='network_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
=======
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
>>>>>>> 9e852cff8f184715319db200de82b4e3f66996de
