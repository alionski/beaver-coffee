# importing specific functions from Flask
from flask import render_template, request, url_for
from flask_mongoengine.wtf import model_form
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


# used for adding documents to a collection
# for example localhost:3031/populate/customers
# will show a form for the customer model
# and clicking "save" will save a document to the database
@app.route("/populate/<collection>", methods=['GET', 'POST'])
def populate(collection):
    # add models here to render them as a form
    model = {"customers": Customer(),
             "employees": Employee()}.get(collection)

    form = model_form(model.__class__)(request.form)
    name = model.__class__.__name__

    if form.validate_on_submit():
        form.populate_obj(model)
        model.save()
        return redirect(url_for("populate", collection=collection))

    return render_template("populate.html", name=name, form=form)


# button in navbar
@app.route("/admin/", methods=['GET'])
def show_admin_page():
    return render_template("admin.html")


@app.route("/admin/action/", methods=['POST'])
def admin_action():
    if "manage_employee" in request.form:
        # do something here
        return render_template("manage_employee.html")
    elif "manage_customer" in request.form:
        # do something here
        return render_template("manage_customer.html")
    elif "manage_stock" in request.form:
        # do something here
        return render_template("manage_stock.html")
    elif "reports" in request.form:
        # do something here
        return render_template("reports.html")


# re-retrieves the available products from the db
def refresh_products():
    products.clear()

    for product in Product.objects:
        # add the product to the list of products
        products[product.name] = product


# called when user adds products to the cart/order
def add_to_order(choices):
    for choice in choices:
        mongo_helper.add_to_order(products[choice])


# submits the order, i.e. pushed to the db
def finish_order():
    mongo_helper.place_order()
    redirect(url_for('index'))
