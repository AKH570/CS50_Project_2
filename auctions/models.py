from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name=models.CharField(max_length=150)

    def __str__(self):
        return self.category_name
      
class Auction_listing(models.Model):
    auctionTitle = models.CharField(max_length=200)
    descriptions = models.TextField(max_length=300)
    auctionImageLink = models.CharField(max_length=700)
    Price = models.FloatField(blank=True,null=True)
    is_Available = models.BooleanField(default=True)
    is_auctionOwner = models.BooleanField(default=False)
    auctionOwner = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    auctionCategory = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    watchlist = models.ManyToManyField(User,blank=True,related_name='watchlist')
    
    def __str__(self):
        return self.auctionTitle
    @property
    def dollar_price(self):
        return "$%s" % self.Price
    
class Comments(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    message = models.CharField(max_length=300,blank=False)
    auctionName = models.ForeignKey(Auction_listing,on_delete=models.CASCADE,blank=True)
    commentDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.userName}'

class Bid(models.Model):
    bid_Name=models.ForeignKey(Auction_listing,on_delete=models.CASCADE,blank=True,null=True,related_name='bidTitleName')
    bidPrice = models.FloatField(default=0,blank=True,null=True)
    bidderName= models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
   
    @property
    def dollar_price(self):
        return "$%s" % self.bidPrice

