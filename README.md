# eAuction

This is online auction based web app.Here two types of user like admin and normal user. Every user has different dashboard. User can create auction item. User can also attened to the Bidding system. Maximum price of auction is the winner of bid.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

##Challenges 
    I have faced some challenges when create this app. At first day i faced input date in aucttion form but i overcome this problem using form filtering with bootstrap framework. Second day, I can't work totally from morning tiil night because of loadshedding.Third problem is create chart in admin dashbord.I can't this solved this problem.


### Installing

A step by step series of examples that tell you how to get a development env running

1. Install Python
    
   Install python-3.7.2 and python-pip. Follow the steps from the below reference document based on your Operating System. Reference: https://docs.python-guide.org    /starting/installation/
2. Setup virtual environment
```
# Install virtual environment
pip install virtualenv

# Make a directory
mkdir envs

# Create virtual environment
virtualenv ./envs/

# Activate virtual environment
source envs/bin/activate

```
3.Install requirements
  ```
  pip install -r requirements.txt
  ```
And repeat

```
python manage.py makemigraitons
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Now you can create auction item and win bid.


## Authors

* **Shafayet Hussain** - *Initial work* - [PurpleBooth](https://github.com/HussainShafayet)


