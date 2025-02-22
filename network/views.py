from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import User, Post, FriendRequest

def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    posts = Post.objects.all().order_by('-timestamp')
    return render(request, 'network/index.html', {'posts': posts})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'network/login.html')

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        password_confirmation = request.POST["password_confirmation"]

        if password != password_confirmation:
            return render(request, "network/register.html", {
                "message": "كلمات المرور غير متطابقة."
            })

        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "اسم المستخدم مستخدم بالفعل."
            })

        login(request, user)
        return redirect("index")

    return render(request, "network/register.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def add_post(request):
    if request.method == "POST":
        content = request.POST.get("body")
        if content:
            Post.objects.create(user=request.user, body=content)
        return redirect("index")
    return render(request, "network/index.html")

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return redirect('index')

@login_required
def users_list(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'network/users.html', {'users': users})

@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if not FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
    return redirect('users')

@login_required
def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.to_user.friends.add(friend_request.from_user)
    friend_request.from_user.friends.add(friend_request.to_user)
    friend_request.delete()
    return redirect('friend_requests')

@login_required
def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    friend_request.delete()
    return redirect('friend_requests')

@login_required
def friend_requests(request):
    requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, "network/friend_requests.html", {"requests": requests})