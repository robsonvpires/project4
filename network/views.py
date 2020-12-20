import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


from .models import *
from .forms import *


def index(request,post=""):

    def getPaginator(posts):
        pages = request.GET.get('page')
        pagination = Paginator(posts, 30) 
        page = pagination.get_page(pages)
        return page
    
    if(post == ""):
        posts = Post.objects.all()
        posts = posts.order_by("-timestamp").all()
        page_obj = getPaginator(posts)
        return render(request , "network/index.html", {
            "page_obj":page_obj,
            "users":User.objects.all()
        })
    
    if request.user.is_authenticated: 
        if post == "following":
            posts = Post.objects.filter(user__in = request.user.following.all())
            posts = posts.order_by("-timestamp").all()
            page_obj = getPaginator(posts)
            return render(request , "network/following.html", {
                "page_obj":page_obj
            })
            
        elif User.objects.filter(username = post):
            user = User.objects.filter(username = post).first()
            posts = Post.objects.filter(user = user)
            posts = posts.order_by("-timestamp").all()
            page_obj = getPaginator(posts)
            return render(request , "network/user.html", {
                "page_obj":page_obj,
                "user":user,
                "followers": user.followers.count(),
                "following": user.following.count(),
                "isfollowing": user in request.user.following.all()
            })

        else:
            return HttpResponse("404 Page Not found")

    else:
        return HttpResponseRedirect(reverse("login"))

@csrf_exempt
@login_required
def create(request):
    
    if request.method == "POST":    
        data = json.loads(request.body)
        body = data.get("body","")
        user = request.user
        post = Post(user = user , body = body)
        post.save()
        return JsonResponse({"message": "Post created successfully."}, status=201)
        
    else:
        return JsonResponse({"error":"Request method not allowed"},status=400)

@csrf_exempt
def post(request , post_id):

    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    
    if request.method == "POST":
        data = json.loads(request.body)
        body = data.get("body","")
        post.body = body
        post.save()
        return JsonResponse({"body": post.body}, status=201)
    
    elif request.method == "PUT":
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            likes = False
        else:
            post.likes.add(request.user)
            likes = True

        count = post.likes.count()
        return JsonResponse({"likes":likes , "count":count})

    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)

@csrf_exempt
def follow(request , user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "Post not found."}, status=404)
    followers = user.followers.count()
    if user!=request.user and request.method == "PUT":
        if user in request.user.following.all():
            request.user.following.remove(user)
            followers = followers-1
            return JsonResponse({"following":False , "count":followers})
        else:
            request.user.following.add(user)
            followers = followers+1
            return JsonResponse({"following":True , "count":followers})


    return redirect("posts", post=user.username)


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
