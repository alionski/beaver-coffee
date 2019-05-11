import pymongo
import configparser

# there should be the file called credentials.ini in the same dir
# see credentials_example.ini
# do not add credentials.ini to git (!)

config = configparser.ConfigParser()
config.read('credentials.ini')
username = config['mongo_atlas']['username']
password = config['mongo_atlas']['password']

client = pymongo.MongoClient("mongodb+srv://" + username + ":" + password + "@cluster0-jwmsg.mongodb.net/test?retryWrites=true")


# define db, does nothing if it's already present
beaver_database = client.beaver
# define collections, doesn nothing if it's already present
products_collection = beaver_database.products
orders_collection = beaver_database.orders

# global lists
prods = []
prices = []


# gets all products from the collection on Atlas
# called from run.py
def get_all_products():
    return products_collection.find()


# adds a product to the cart, done when the user clicks "add to order"
# called from run.py
def add_to_order(product_name, price):
    prods.append(product_name)
    prices.append(price)


# adds the order to the db, called from run.py when the user clicks
# "Checkout order"
def place_order():
    total_price = 0
    for price in prices:
        total_price += int(price)

    order = {
        "sales_items": prods,
        "total_price": total_price
    }
    orders_collection.insert_one(order)
    # make sure it's empty after the order is committed
    # to not mess up with the next order
    # global variables are questionable solution but works for now
    prods.clear()
    prices.clear()

