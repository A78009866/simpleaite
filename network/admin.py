from django.contrib import admin

from .models import User, Post, Like, Follower

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "body", "timestamp")


admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Follower)