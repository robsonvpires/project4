
from django.urls import path
from . import views

urlpatterns = [
    path("user/<int:user_id>", views.follow, name="follow"),
    path("post", views.create , name = "create"),
    path("like/<int:post_id>", views.post , name="post"),
    path("posts/<str:post>", views.index, name="posts"),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]
