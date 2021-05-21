from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Auction_item(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Name=models.CharField(max_length=50)
    Description=models.TextField()
    Photo=models.ImageField(upload_to='images/others')
    Price=models.IntegerField()
    DateTime=models.DateTimeField()
    active=models.BooleanField(default=True)

    def __str__(self):
        return self.Name

class Bid(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    item=models.ForeignKey(Auction_item,on_delete=models.CASCADE)
    description=models.TextField()
    bid=models.IntegerField()
    active=models.BooleanField(default=True)

    def __str__(self):
        return str(self.item)
    

   
    
    