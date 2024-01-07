from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Category,Auction_listing,Comments,Bid,auctionWinner
from .models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def allListing(request):
     activeAuction= Auction_listing.objects.all()
     categories = Category.objects.all()
     return render(request, "auctions/listingall.html",
                  {'Auctions':activeAuction,
                   'category':categories })

def listingAuction(request,id):
        login_view(request)
        activeAuction = Auction_listing.objects.get(pk=id)
        # if new auction having no bid
        try: 
            NewBid = Bid.objects.get(bid_Name=activeAuction)
        except Bid.DoesNotExist:
             NewBid = Bid.objects.all()
        autionReviews = Comments.objects.filter(auctionName=activeAuction).order_by('-commentDate')
        isWatchListExist = request.user in activeAuction.watchlist.all()
        isOwner=activeAuction.auctionOwner==request.user
        if activeAuction.is_Available==False and NewBid.bidderName==request.user:
                messages.success(request,'Congratulations! You are winner of this auction')
        return render(request, "auctions/listing.html",
                {
                'Auctions':activeAuction,
                'isWatchListExist':isWatchListExist,
                'reviews':autionReviews,
                'newBid':NewBid,
                'auctionOwner':isOwner
                })
   
def bidAuction(request,id):
        PlaceBid = request.POST.get('new_bid') 
        activeAuction = Auction_listing.objects.get(pk=id)
        existinBid = Bid.objects.get(bid_Name=activeAuction)
        autionReviews = Comments.objects.filter(auctionName=activeAuction).order_by('-commentDate')
        if float(PlaceBid) > activeAuction.Price: 
            if existinBid.bidPrice==0.0:
                Bid.objects.filter(bid_Name=activeAuction).update(bidPrice=PlaceBid,bidderName=request.user)
                UpdatedBid = Bid.objects.get(bid_Name=activeAuction)

                messages.success(request,'New bid successfully updated') 
                return render(request, "auctions/listing.html",
                                    {
                                    'Auctions':activeAuction,
                                    'reviews':autionReviews,
                                    'newBid':UpdatedBid,
                                    }) 
        
            elif float(PlaceBid) > existinBid.bidPrice: 
                messages.success(request,'Your bid successfully updated')      
                Bid.objects.filter(bid_Name=activeAuction).update(bidPrice=PlaceBid,bidderName=request.user)
                UpdatedBid = Bid.objects.get(bid_Name=activeAuction)
                return render(request, "auctions/listing.html",{
                    'Auctions':activeAuction,
                    'reviews':autionReviews,
                    'newBid':UpdatedBid,
                })
            elif existinBid.bidPrice > float(PlaceBid) > activeAuction.Price:
                messages.error(request,'Your Bid is less than present price')
                UpdatedBid = Bid.objects.get(bid_Name=activeAuction)
                return render(request, "auctions/listing.html",{
                    'Auctions':activeAuction,
                    'reviews':autionReviews,
                    'newBid':UpdatedBid,
                })
        else:
             messages.error(request,'Your Bid is less than present price')
             UpdatedBid = Bid.objects.get(bid_Name=activeAuction)
             return render(request, "auctions/listing.html",{
                'Auctions':activeAuction,
                'reviews':autionReviews,
                'newBid':UpdatedBid,
            })

def  closeAuction(request,id):
        if request.method == 'POST':    
            activeAuction = Auction_listing.objects.get(pk=id)
            activeAuction.is_Available=False
            activeAuction.save()
            autionReviews = Comments.objects.filter(auctionName=activeAuction).order_by('-commentDate')
            #isWatchListExist = request.user in activeAuction.watchlist.all()
            isOwner=activeAuction.auctionOwner==request.user
            NewBid = Bid.objects.get(bid_Name=activeAuction)
            wonUsername=NewBid.bidderName
            wonbidprice=NewBid.bidPrice
            wininfo=auctionWinner(
                    winAuction=activeAuction,
                    winner=wonUsername,
                    winBid=wonbidprice, )                      
            wininfo.save()
            activeAuction.auctionOwner=wininfo.winner
            activeAuction.save()
            messages.success(request,'Congratulations! Your auction is closed.')
            return render(request, "auctions/listing.html",
                    {
                    'Auctions':activeAuction,
                    #'isWatchListExist':isWatchListExist,
                    'reviews':autionReviews,
                    'newBid':NewBid,
                    'auctionOwner':isOwner
                    })
        else:
             return
def Reviews(request,id):
        comment=request.POST['comment']
        user=request.user
        activeAuction = Auction_listing.objects.get(pk=id)

        newComment = Comments(
            author = user,
            message = comment,
            auctionName=activeAuction
        )
        newComment.save()

        return HttpResponseRedirect(reverse(listingAuction,args=(id, )))

def RemoveList(request,id):
    activeAuction = Auction_listing.objects.get(pk=id)
    activeAuction.watchlist.remove(request.user)
    return HttpResponseRedirect(reverse(listingAuction,args=(id, )))

def AddList(request,id):
    activeAuction = Auction_listing.objects.get(pk=id)
    activeAuction.watchlist.add(request.user)
    return HttpResponseRedirect(reverse(listingAuction,args=(id, )))

def watchList(request):
    #activeUser = request.user
    activeAuction= request.user.watchlist.all()
    return render (request,'auctions/watchlist.html',
                   {'Auctions':activeAuction})

def categoryItem(request,id):
        try:
            categoryName = Category.objects.get(pk=id)
            categories = Category.objects.all()
            activeAuction = Auction_listing.objects.filter(auctionCategory=categoryName,is_Available=True)
            return render(request, "auctions/index.html",
                    {
                    'Auctions':activeAuction,
                    'category':categories,
                    })
        except Auction_listing.objects.get(auctionCategory=categoryName).DoesNotExist:
             pass
             
def index(request):
    activeAuction= Auction_listing.objects.filter(is_Available=True)
    categories = Category.objects.all()
    return render(request, "auctions/index.html",
                  {'Auctions':activeAuction,
                   'category':categories })


def createAuction(request):
    if request.method =='POST':
        title = request.POST['title']
        descriptions = request.POST['message']
        image = request.POST['image']
        price = request.POST['price']
        cat = request.POST['category']
        aucOwner = request.user

        categoryItem= Category.objects.get(category_name=cat)

        newList = Auction_listing(
            auctionTitle=title,
            descriptions=descriptions, 
            auctionImageLink= image,
            Price=price,
            auctionCategory = categoryItem,
            auctionOwner=aucOwner,
            is_auctionOwner=True
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
