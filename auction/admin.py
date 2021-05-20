from django.contrib import admin
from .models import Auction_item,Bid

# Register your models here.
admin.site.register(Auction_item)
admin.site.register(Bid)
