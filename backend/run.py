# importing specific functions from Flask
from flask import Flask, render_template, request, url_for
# this is marked red in my IDE for a mysterious reason but it should be imported this way
# for it work bc it's in the same package -- we are importing the whole module here
import mongo_helper
# we are importing one function here only
from werkzeug.utils import redirect

# this is how define a new Flask app
app = Flask(__name__)

# global vars
# list(array) of products the way it is in the db
products_collection = []
# a dictionary (sort of like java's map) with mappings like: "latte" : "5"
prices = {}
# list of products, like: "coffee", "cappuccino", "latte" etc.
products = []


# main page, returned when one navigates to 127.0.0.1
# when you type http://127.0.0.1, this method will be called
@app.route("/", methods=['GET'])
def main():
    # first get all products from the db and organize them
    refresh_products()
    return render_template("main.html", products=products, prices=prices)


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
        return render_template("main.html", products=products, prices=prices, choices=choices)
    # user clicked "Checkout"
    elif "checkout" in request.form:
        # add the order to the db
        finish_order()
        # go back to a clean main page
        return redirect(url_for('main'))


# re-retrieves the available products from the db
def refresh_products():
    products_collection = mongo_helper.get_all_products()
    prices.clear()
    products.clear()
    for prod in products_collection:
        # add prices to the dict with product names as keys
        prices[prod["name"]] = prod["price"]
        # add the product to the list of products
        products.append(prod["name"])


# called when user adds products to the cart/order
def add_to_order(choices):
    for choice in choices:
        mongo_helper.add_to_order(choice, prices[choice])


# submits the order, i.e. pushed to the db
def finish_order():
    mongo_helper.place_order()
    redirect(url_for('main'))


# this is Flask-specific, the main method
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
