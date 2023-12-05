from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    pass

class Category(models.Model):
    category_name=models.CharField(max_length=150)

    def __str__(self):
        return self.category_name

class auction_listing(models.Model):
    title = models.CharField(max_length=200)
    descriptions = models.TextField(max_length=300)
    imageLink = models.CharField(max_length=700)
    price = models.IntegerField()
    is_Available = models.BooleanField(default=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    watchlist = models.ManyToManyField(User,blank=True,related_name='watchlist')
    
    def __str__(self):
        return self.title
    
class Comments(models.Model):
    userName = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    message = models.CharField(max_length=300,blank=False)
    auctionName = models.ForeignKey(auction_listing,on_delete=models.CASCADE,blank=True)
    commentDate = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.userName}'


