
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:username>", views.profile_view, name="profile"),
    path("follow_user/<int:user_id>/<int:current_user_id>", views.follow_user, name="follow_user"),
    path("unfollow_user/<int:user_id>", views.unfollow_user, name="unfollow_user"),
    path("<str:username>/following", views.following_view, name="following"),
    path("like/<int:post_id>", views.like_post, name="like_post"),
    path("unlike/<int:post_id>", views.unlike_post, name="unlike_post"),

    # API Routes
    path("posts", views.new_post, name="new_post"),
    path("posts/<int:post_id>", views.post, name="post"),
    path("profile/user/<int:user_id>", views.user_posts, name="user_posts"),
    path("all_posts", views.all_posts, name="all_posts"),
    path("user_info/<int:user_id>", views.user_info, name="user_info"),
    path("profile/update_post/<int:post_id>", views.update_post_body, name="update_post"),
    path("update_post/<int:post_id>", views.update_post_body, name="update_post_index")
]
