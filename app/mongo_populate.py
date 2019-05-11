# this is not part of the app
# I used this file to add collections and push some
# products to the product collection
# I commented and uncommented stuff and did some
# db administration so to speak
# ran it by simply $ python mongo_populate.py

from mongoengine import connect
from app.models import *
import configparser

config = configparser.ConfigParser()
config.read('app/credentials.ini')
username = config['mongo_atlas']['username']
password = config['mongo_atlas']['password']
atlas_uri = "mongodb+srv://" + username + ":" + password + "@cluster0-jwmsg.mongodb.net/beaver?retryWrites=true"

connect('beaver', atlas_uri)

# I've been deleting and rewriting here so it's not all the
# stuff that I've run

hot_chocolate = {
    "name": "hot chocolate",
    "price": "4",
}

avocado_latte = {
    "name": "avocado latte",
    "price": "10"
}

to_insert = [hot_chocolate, avocado_latte]
for p in to_insert:
    Product(name=p['name'], price=p['price']).save()
