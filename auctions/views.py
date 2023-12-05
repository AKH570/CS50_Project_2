from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Category,auction_listing,Comments
from .models import User



def Listing(request,id):
    try:
        activeAuction = auction_listing.objects.get(pk=id)
        autionReviews = Comments.objects.filter(auctionName=activeAuction).order_by('-commentDate')
        #print(f'this is all comments:{autionReviews}')
        isWatchListExist = request.user in activeAuction.watchlist.all()
        return render(request, "auctions/listing.html",
                {
                'Auctions':activeAuction,
                'isWatchListExist':isWatchListExist,
                'reviews':autionReviews,
                })
    
    except Exception as e:
       return HttpResponse('This item is not exist')
    

def Reviews(request,  id):
        comment= request.POST['comment']
        user=request.user
        activeAuction = auction_listing.objects.get(pk=id)

        newComment = Comments(
            userName = user,
            message = comment,
            auctionName=activeAuction
        )
        newComment.save()

        return HttpResponseRedirect(reverse(Listing,args=(id, )))

def RemoveList(request,id):
    activeAuction = auction_listing.objects.get(pk=id)
    activeAuction.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse(Listing,args=(id, )))

def AddList(request,id):
    activeAuction = auction_listing.objects.get(pk=id)
    activeAuction.watchlist.add(request.user)
    return HttpResponseRedirect(reverse(Listing,args=(id, )))

def watchList(request):
    #activeUser = request.user
    activeAuction= request.user.watchlist.all()
    print(f'this is watchlist {activeAuction}')
    return render (request,'auctions/watchlist.html',
                   {'Auctions':activeAuction})

def categoryItem(request,category_name):
    try:
        categoryName = Category.objects.get(category_name=category_name)
        activeAuction = auction_listing.objects.filter(is_Available=True,category=categoryName)
        categories = Category.objects.all()
        return render(request, "auctions/index.html",
                {
                'Auctions':activeAuction,
                'category':categories,
                })
    
    except Exception as e:
        return HttpResponse('This item is not exist')
    

def index(request):
    activeAuction= auction_listing.objects.filter(is_Available=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",
                  {'Auctions':activeAuction,
                   'category':categories })


def CreateListing(request):
    if request.method =='POST':
        title = request.POST['title']
        descriptions = request.POST['message']
        image = request.POST['image']
        price = request.POST['price']
        cat = request.POST['category']
        user = request.user

        categoryItem= Category.objects.get(category_name=cat)

        newList = auction_listing(
            title=title,
            descriptions=descriptions, 
            imageLink= image,
            price=price,
            category = categoryItem,
            user=user
            )
        newList.save()

        return HttpResponseRedirect(reverse(index))
    else: 
        category = Category.objects.all()
    
    return render(request,'auctions/createlisting.html',{'categories':category})


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
