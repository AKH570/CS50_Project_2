from django.urls import path

from . import views

urlpatterns = [
    path("", views.allListing, name="listingall"),
    path("activelisting", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("creatlist", views.createAuction, name="creatlist"),
    path("catitem/<int:id>", views.categoryItem, name="cateitem"),
    path("listing/<int:id>", views.listingAuction, name="listing"),
    path("removelist/<int:id>", views.RemoveList, name="removelist"),
    path("addlist/<int:id>", views.AddList, name="addlist"),
    path("watchlist", views.watchList, name="watchlist"),
    path("reviews/<int:id>", views.Reviews, name="reviews"),
    path("bid/<int:id>", views.bidAuction, name="Newbid"),
    path("closeAuc/<int:id>",views.closeAuction, name='closeAuc'),
]
