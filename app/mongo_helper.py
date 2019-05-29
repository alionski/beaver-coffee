from app.models import Product, Order

# global lists
products = []


# gets all products from the collection on Atlas
# called from routes.py
def get_all_products():
    return Product.objects


# adds a product to the cart, done when the user clicks "add to order"
# called from routes.py
def add_to_order(product):
    products.append(product)


# adds the order to the db, called from routes.py when the user clicks
# "Checkout order"
def place_order():
    total_price = 0
    sales_items = []
    for p in products:
        total_price += int(p.price)

        # copy the product information to sales_items
        # we don't want to reference the product document in the db
        # since it might change in the future
        sales_items.append({"name": p.name, "price": p.price})

    Order(sales_items=sales_items, total_price=total_price).save()

    # make sure it's empty after the order is committed
    # to not mess up with the next order
    # global variables are questionable solution but works for now
    products.clear()

# only clears order dont know if it should do something more
def cancel_order():
    products.clear()
