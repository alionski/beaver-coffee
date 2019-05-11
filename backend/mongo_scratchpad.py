# this is not part of the app
# I used this file to add collections and push some
# products to the product collection
# I commented and uncommented stuff and did some
# db administration so to speak
# ran it by simply $ python mongo_scratchpad.py

import pymongo
import configparser

config = configparser.ConfigParser()
config.read('credentials.ini')
username = config['mongo_atlas']['username']
password = config['mongo_atlas']['password']

client = pymongo.MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0-jwmsg.mongodb.net/test?retryWrites=true")

# define db
beaver_database = client.beaver
# define collections
products_collection = beaver_database.products
orders_collection = beaver_database.orders

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
products_collection.insert_many(to_insert)