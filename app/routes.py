# importing specific functions from Flask
from flask import render_template, request, url_for
from werkzeug.utils import redirect
from app import app, mongo_helper
from app.models import *

# list of products, like: "coffee", "cappuccino", "latte" etc.
products = {}


# main page, returned when one navigates to 127.0.0.1
# when you type http://127.0.0.1, this method will be called
@app.route("/", methods=['GET'])
def index():
    # first get all products from the db and organize them
    refresh_products()
    return render_template("index.html", products=products.values())


# this will be called when the user clicks on "Add to order" or "Checkout"
# it adds the checked products to card and adds them to the
# lists in mongo_helper.py in the first case
# or places the order in the second case
@app.route("/", methods=['POST'])
def update_order():
    # this is how we are getting the values from html checkboxes
    choices = request.form.getlist("checkbox_products")
    # user clicked "Add to order"
    if "add_to_order" in request.form:
        add_to_order(choices)
        # show updates and keep the checkboxes clicked
        return render_template("index.html", products=products.values(), choices=choices)
    # user clicked "Checkout"
    elif "checkout" in request.form:
        # add the order to the db
        finish_order()
        # go back to a clean main page
        return redirect(url_for('index'))


# re-retrieves the available products from the db
def refresh_products():
    products.clear()

    for product in Product.objects:
        print(product.name, ":", product.price)
        # add the product to the list of products
        products[product.name] = product


# called when user adds products to the cart/order
def add_to_order(choices):
    for choice in choices:
        print(choice)
        mongo_helper.add_to_order(products[choice])


# submits the order, i.e. pushed to the db
def finish_order():
    mongo_helper.place_order()
    redirect(url_for('index'))
