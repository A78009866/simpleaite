import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Follower, Like


def index(request):
    posts = Post.objects.all()
    reversed_posts = posts[::-1]
    paginator = Paginator(reversed_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    user_likes_post_ids = []
    if request.user.is_authenticated:
        user_likes = Like.objects.all().filter(user=request.user)
        for like in user_likes:
            user_likes_post_ids.append(like.post.id)
    return render(request, "network/index.html", {
        "page_obj": page_obj,
        "user_likes_post_ids": user_likes_post_ids
    })

@login_required
def following_view(request, username):
    user = User.objects.get(username=username)
    all_posts = Post.objects.all()
    posts = []

    # Get a list of all folowees
    following_followers = user.following.all()
    following_users = []
    for follower in following_followers:
        following_users.append(follower.followee)

    # Adds posts from people the user is following to the list
    for post in all_posts:
        if post.user in following_users:
            posts.append(post)

    # Sets the posts in reverse chronological order
    reversed_posts = posts[::-1]

    # Pagination
    paginator = Paginator(reversed_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Likes
    user_likes_post_ids = []
    user_likes = Like.objects.all().filter(user=request.user)
    for like in user_likes:
        user_likes_post_ids.append(like.post.id)

    return render(request, "network/following.html", {
        "page_obj": page_obj,
        "user_likes_post_ids": user_likes_post_ids
    })


def profile_view(request, username):
    user = User.objects.get(username=username)
    user_likes_post_ids = []
    if request.user.is_authenticated:
        user_likes = Like.objects.all().filter(user=request.user)
        for like in user_likes:
            user_likes_post_ids.append(like.post.id)
    posts = user.user_posts.all()
    reversed_posts = posts[::-1]
    followers = user.followers.all()
    users = []
    for follower in followers:
        users.append(follower.follower)
    # Pagination
    paginator = Paginator(reversed_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "network/profile.html", {
        "user": user,
        "page_obj": page_obj,
        "user_likes_post_ids": user_likes_post_ids,
        "followers": users,
        "followerscount": len(user.followers.all()),
        "followingcount": len(user.following.all())
    })


# Like the post whose button was clicked on
@login_required
def like_post(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)

    # Get list of current post likes to check if user already likes post
    likes_check = post.post_likes.all()
    likes_check_users = []
    for each_like in likes_check:
        likes_check_users.append(each_like.user)

    # If not already liked post
    if user not in likes_check_users:
        # Create the like
        like = Like(user=user, post=post)
        like.save()
        # Add the like to the post likes
        post.likes.add(like)

    return profile_view(request, post.user.username)


@login_required
def unlike_post(request, post_id):
    user = request.user
    post = Post.objects.get(pk=post_id)

    # Get list of current likes to see if like exists
    likes_check = post.likes.all()
    users_check = []
    for like_check in likes_check:
        users_check.append(like_check.user)
    if user in users_check:
        # Get like instance
        like = Like.objects.get(user=user, post=post)
        post.likes.remove(like)
        like.delete()

    return profile_view(request, post.user.username)


# Follow user whose button was clicked on in their profile
@login_required
def follow_user(request, user_id, current_user_id):
    current_user = User.objects.get(pk=current_user_id)
    user_to_follow = User.objects.get(pk=user_id)

    # Get list of current followers to check if user is already following
    followers_check = user_to_follow.followers.all()
    users_check = []
    for follower_check in  followers_check:
        users_check.append(follower_check.follower)

    # If not already following
    if current_user not in users_check:
        # Create follower instance
        follower = Follower(follower=request.user, followee=user_to_follow)
        follower.save()
        # Add the Follower to the user's followers list
        user_to_follow.followers.add(follower)
        # Add the Follower to the signed in user's following list
        current_user.following.add(follower)

    return profile_view(request,user_to_follow.username)

# Unfollow user whose  button was clicked on in their profile
@login_required
def unfollow_user(request, user_id):
    current_user = request.user
    user_to_unfollow = User.objects.get(pk=user_id)

    # Get list of current followers to check if follower object exists
    followers_check = user_to_unfollow.followers.all()
    users_check = []
    for follower_check in  followers_check:
        users_check.append(follower_check.follower)

    if current_user in users_check:
        # Get follower instance
        follower = Follower.objects.get(follower=current_user, followee=user_to_unfollow)
        user_to_unfollow.followers.remove(follower)
        current_user.following.remove(follower)
        follower.delete()

    return profile_view(request, user_to_unfollow.username)



# API - Gets the users id, username, number following, and number of followers
def get_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    return JsonResponse(user.serialize())


# API - Gets the currently logged in user
def user_info(request, user_id):
    user = User.objects.get(pk=user_id)
    return JsonResponse(user.serialize())


# API - Creates a new post and returns to the All Posts view
@login_required
def new_post(request):

    # Get contents of post
    data = json.loads(request.body)
    body = data.get("body", "")
    # Create the new post and POST
    post = Post.objects.create(user=request.user, body=body)
    return JsonResponse({"message": "Post successful!"}, status=201)

# API - Gets a post based on post id
def post(request, post_id):

    #Query for requested post
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error: Post not found."}, status=404)

    # Return post contents
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Post must be via GET
    else:
        return JsonResponse({
            "error": "GET request required."
        }, status=400)


# API - Replaces the post text with the edited text
def update_post_body(request, post_id):
    post = Post.objects.get(pk=post_id)
    data = json.loads(request.body)
    if data.get("body") != "":
        post.body = data["body"]
    post.save()
    return JsonResponse({"message": "Edit successful!"}, status=201)
    


# API - Gets all posts and returns them in reverse chronological order
def all_posts(request):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


# API - Gets all the posts from a specified user
def user_posts(request, user_id):
    
   # Query for requested user
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)

    posts = Post.objects.all().filter(user=user)
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")