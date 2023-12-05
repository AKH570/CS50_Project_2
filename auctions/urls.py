from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("creatlist", views.CreateListing, name="creatlist"),
    path("catitem/<str:category_name>", views.categoryItem, name="cateitem"),
    path("listing/<int:id>", views.Listing, name="listing"),
    path("removelist/<int:id>", views.RemoveList, name="removelist"),
    path("addlist/<int:id>", views.AddList, name="addlist"),
    path("watchlist", views.watchList, name="watchlist"),
    path("reviews/<int:id>", views.Reviews, name="reviews"),
]
