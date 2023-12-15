from django.contrib import admin
from . models import User, Category,Auction_listing,Comments,Bid
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Auction_listing)
admin.site.register(Comments)

class BidAdmin(admin.ModelAdmin):
    list_display = ['bid_Name','bidPrice','bidderName']
admin.site.register(Bid,BidAdmin)