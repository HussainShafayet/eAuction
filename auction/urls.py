from django.urls import path
from . import views

urlpatterns = [
    path('auction_items', views.auction_items, name='auction_items'),
    path('complete_auctions/', views.complete_auctions_list, name='complete_auctions'),
    path('complete_bid/<int:id>/', views.complete_bids, name='complete_bid'),
    path('auction_create', views.create_auction, name='auction_create'),
    path('my_auction_itmes/', views.user_items, name='user_items'),
    path('edit/my_auction_itmes/<int:id>/', views.edit_user_items, name='edit_user_items'),
    path('item_details/<int:id>', views.item_details, name='item_details'),
    path('item_details/bid_list/<int:id>',views.bid_list,name='bid_list'),
    path('item_details/bid_details/<int:id>',views.bid_details,name='bid_details'),
    path('my_bid',views.my_bid,name='my_bid'),
    path('edit_my_bid/<int:id>',views.edit_my_bid,name='edit_my_bid'),
]
