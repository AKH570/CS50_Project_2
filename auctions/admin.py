from django.contrib import admin
from . models import User, Category,Auction_listing,Comments,Bid,auctionWinner
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction_listing)

class CommentsAdmin(admin.ModelAdmin):
    list_display=['author','message','auctionName','commentDate']
admin.site.register(Comments,CommentsAdmin)

class BidAdmin(admin.ModelAdmin):
    list_display = ['bid_Name','bidPrice','bidderName']
admin.site.register(Bid,BidAdmin)

class WinneerAdmin(admin.ModelAdmin):
    list_display = ['winAuction','winBid','winner','WinningDate']
admin.site.register(auctionWinner,WinneerAdmin)