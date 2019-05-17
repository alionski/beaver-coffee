from mongoengine import *
import datetime


COUNTRY = [('swe', "Sweden"), ("usa", "United States"), ("gbr", "Great Britain")]
CURRENCY = [('sek', "SEK"), ("usd", "USD"), ("gbp", "GBP")]
LANGUAGE = [('swe', "Swedish"), ("eng", "English")]
POSITION = [("employee", "Employee"), ("location_manager", "Location Manager"), ("sales_manager", "Sales Manager")]
PRODUCT_TYPE = [('drink', "Drink"), ("whole_bean", "Whole Bean"), ("extra", "Extra")]


class LocalizedField(EmbeddedDocument):
    swe = StringField()
    eng = StringField()

    def __repr__(self):
        return "<LocalizedField {0}, {1}>".format(self.swe, self.eng)


class Address(EmbeddedDocument):
    city = StringField(max_length=20)
    street_name = StringField(max_length=100)
    zip_code = StringField(max_length=10)

    def __repr__(self):
        return "<Address {0}, {1}, {2}>".format(self.street_name, self.zip_code, self.city)


class Product(Document):
    meta = {'collection': 'products'}
    name = StringField(required=True)
    price = IntField(min_value=0)


class Order(Document):
    meta = {'collection': 'orders'}
    timestamp = DateTimeField(default=datetime.datetime.utcnow)
    sales_items = ListField(DictField())
    total_price = IntField(min_value=0)


class Location(Document):
    meta = {'collection': 'locations'}
    currency = StringField(required=True, max_length=3, choices=CURRENCY)
    country = StringField(required=True, max_length=3, choices=COUNTRY)
    language = StringField(required=True, max_length=3, choices=LANGUAGE)
    address = EmbeddedDocumentField(Address)

    def __repr__(self):
        return "<Location {0}, {1}>".format(self.country, self.address)


class Membership(EmbeddedDocument):
    country = StringField(required=True, max_length=3, choices=COUNTRY)
    barcode = StringField(required=True, max_length=13, default="0123456789123")


class Customer(Document):
    meta = {'collection': 'customers'}
    first_name = StringField(max_length=20, required=True)
    last_name = StringField(max_length=20, required=True)
    ssn = StringField(max_length=11, required=True)
    occupation = StringField(max_length=30)
    address = EmbeddedDocumentField(Address)
    membership = EmbeddedDocumentField(Membership, required=True)

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def __repr__(self):
        return "<Customer {}>".format(self.get_full_name())


class Employment(EmbeddedDocument):
    start_date = DateTimeField(default=datetime.datetime.utcnow, required=True)
    end_date = DateTimeField(default=datetime.datetime.utcnow, required=True)
    position = StringField(default=POSITION[0], choices=POSITION, required=True)
    percentage_full_time = IntField(min_value=0, max_value=100, default=100, required=True)
    location = ReferenceField(Location, required=True)


class Comment(EmbeddedDocument):
    created = DateTimeField(default=datetime.datetime.utcnow)
    text = StringField(max_length=300, required=True)
    author = StringField(required=True)


class Employee(Document):
    meta = {'collection': 'employees'}
    first_name = StringField(max_length=20, required=True)
    last_name = StringField(max_length=20, required=True)
    address = EmbeddedDocumentField(Address)
    comments = EmbeddedDocumentListField(Comment)
    employment = EmbeddedDocumentField(Employment, required=True)
    employment_history = EmbeddedDocumentListField(Employment)

    def add_comment(self, comment):
        self.comments.append(comment)
        self.save()

    def set_employment(self, employment):
        self.employment_history.append(self.employment)
        self.employment = employment
        self.save()

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def __repr__(self):
        return "<Employee {}>".format(self.get_full_name())
