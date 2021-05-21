from django import forms
from .models import Auction_item, Bid


class Auction_item_Form(forms.ModelForm):
    class Meta():
        model = Auction_item
        fields = ['Name', 'Description', 'Price', 'DateTime', 'Photo', ]
        exclude = ['active']
        labels = {
            'Name': 'Product Name',
            'Description': 'Product Description',
            'Photo': 'Product Photo',
            'Price': 'Minimum Bid Price',
            'DateTime': 'End DateTime',
        }
        widgets = {
            'Description': forms.Textarea(attrs={'rows': 2, 'cols': 6}),
            'DateTime': forms.DateInput(format=('%m/%d/%Y '),
                                        attrs={'class': 'form-control',   'placeholder': 'Select a date', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(Auction_item_Form, self).__init__(*args, **kwargs)

        self.fields['Name'].widget.attrs.update({

            'placeholder': 'Name',
        })
        self.fields['Description'].widget.attrs.update({

            'placeholder': '(Maximum 500 words)'
        })
        self.fields['Price'].widget.attrs.update({

            'placeholder': 'Bid Price',

        })


class Bid_Form(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            'description', 'bid'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 1, 'cols': 4})
        }
