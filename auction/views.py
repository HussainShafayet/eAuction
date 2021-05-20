from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import Auction_item_Form, Bid_Form
from .models import Auction_item, Bid
from django.db.models import Max, Sum

# Create your views here.

from datetime import datetime


def auction_items(request):
    items = Auction_item.objects.filter(active=True)
    count = Auction_item.objects.filter(active=True).count()
    total_value = Auction_item.objects.filter(
        active=True).aggregate(Sum('Price'))
    today = datetime.now().date()
    new_list = []
    for auction in items:
        auction.DateTime = auction.DateTime.date()
        bid_items = auction.bid_set.all()
        if today == auction.DateTime or today > auction.DateTime:
            for j in bid_items:
                j.active = False
                j.save()
            auction.active = False
            auction.save()
        new_list.append(auction)

    contex = {
        'today': today,
        'new_list': new_list,
        'count': count,
        'tatal_value': total_value,
    }
    return render(request, 'auction_items.html', contex)


def complete_auctions_list(request):
    complete = Auction_item.objects.filter(active=False)
    today = datetime.now().date

    if not complete:
        messages.warning(request, 'No auction')
        context = {
            'complete': complete,
            'today': today,
        }
        return render(request, 'complete_auctions.html', context)

    else:
        context = {
            'complete': complete,
            'today': today,
        }
        return render(request, 'complete_auctions.html', context)


def complete_bids(request, id):
    item = Auction_item.objects.get(id=id)
    bids = Bid.objects.filter(item=item).aggregate(Max('bid'))
    highest_bid = bids.get('bid__max')
    winner_bid = Bid.objects.get(bid=highest_bid, active=False)

    context = {
        'winner_bid': winner_bid,
    }
    return render(request, 'complete_bid.html', context)


def create_auction(request):
    if request.method == 'POST':
        form = Auction_item_Form(request.POST, request.FILES or None)
        if form.is_valid():
            new_auctions = Auction_item()
            new_auctions.user = request.user
            new_auctions.Name = form.cleaned_data['Name']
            new_auctions.Description = form.cleaned_data['Description']
            new_auctions.Price = form.cleaned_data['Price']
            new_auctions.DateTime = form.cleaned_data['DateTime']
            new_auctions.Photo = form.cleaned_data['Photo']
            new_auctions.save()
            messages.success(request, 'Added Successfull.')
            return redirect('auction_items')
        else:
            value = 'Form'
            contex = {
                'form': form,
                'value': value
            }
            return render(request, 'auction_items.html', contex)
    else:
        form = Auction_item_Form()
        value = 'Form'
        context = {
            'form': form,
            'value': value
        }
        return render(request, 'auction_items.html', context)


def user_items(request):
    items = Auction_item.objects.filter(user=request.user, active=True)
    today = datetime.now().date()
    new_list = []
    for auction in items:
        auction.DateTime = auction.DateTime.date()
        if today == auction.DateTime or today > auction.DateTime:
            auction.active = False
            auction.save()
        new_list.append(auction)

    context = {
        'today': today,
        'new_list': new_list
    }
    return render(request, 'my_items.html', context)


def edit_user_items(request, id):
    item = Auction_item.objects.get(id=id, active=True)
    if request.method == 'POST':
        form = Auction_item_Form(request.POST or None,
                                 request.FILES or None, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated Successfully.')
            return redirect('user_items')
    else:
        form = Auction_item_Form(instance=item)
        value = 'edit_user_item'
        context = {
            'form': form,
            'value': value,
        }
        return render(request, 'auction_items.html', context)


def item_details(request, id):
    if request.method == 'POST':
        user = request.user
        item = Auction_item.objects.get(id=id)
        form = Bid_Form(request.POST)
        if form.is_valid():
            test = Bid.objects.filter(user=user, item=item)
            if not test:
                if user == item.user:
                    messages.warning(
                        request, 'This is your auctoin item. You can not bid.')
                    return redirect('bid_list', id)
                else:
                    new_bid = Bid()
                    new_bid.user = user
                    new_bid.item = item
                    new_bid.description = form.cleaned_data['description']
                    new_bid.bid = form.cleaned_data['bid']
                    new_bid.save()
                    messages.success(request, 'Bidding successfully.')
                    return redirect('bid_list', id)
            else:
                messages.warning(request, 'You Completed Bid already.')
                item_details = 'item_details'
                context = {
                    'item': item,
                    'form': form,
                    'item_details': item_details
                }
                return render(request, 'auction_page.html', context)

        else:
            item_details = 'item_details'
            context = {
                'item': item,
                'form': form,
                'item_details': item_details
            }
            return render(request, 'auction_page.html', context)
    else:
        item = Auction_item.objects.get(id=id)
        form = Bid_Form()
        item_details = 'item_details'
        context = {
            'item': item,
            'item_details': item_details,
            'form': form,
        }
        return render(request, 'auction_page.html', context)


def bid_list(request, id):
    item = Auction_item.objects.get(id=id)
    today = datetime.now().date()
    list_of_bid = Bid.objects.filter(active=True, item=item).order_by('-bid')
    context = {
        'list_of_bid': list_of_bid,
        'item': item,
        'today': today,
    }
    return render(request, 'auction_page.html', context)


def my_bid(request):
    bids = Bid.objects.filter(user=request.user, active=True)
    today = datetime.now().date()
    context = {
        'bids': bids,
        'today': today,
    }
    return render(request, 'bid_list.html', context)


def edit_my_bid(request, id):
    bid = Bid.objects.get(id=id, active=True)
    if request.method == 'POST':
        form = Bid_Form(request.POST, instance=bid)
        if form.is_valid():
            form.save()
            return redirect('my_bid')
    else:
        bid_item = bid.item
        item = Auction_item.objects.get(id=bid_item.id)
        form = Bid_Form(instance=bid)
        context = {
            'item': item,
            'form': form,
        }
        return render(request, 'edit_my_bid.html', context)


def bid_details(request, id):
    bid = Bid.objects.get(id=id)
    bid_item = bid.item
    auction_item = Auction_item.objects.get(id=bid_item.id)
    today = datetime.now().date()
    context = {
        'bid': bid,
        'item': auction_item,
        'today': today,
    }
    return render(request, 'bid_details.html', context)
