from mongoengine import *
import datetime


class Product(Document):
    meta = {'collection': 'products'}
    name = StringField(required=True)
    price = IntField(min_value=0)


class Order(Document):
    meta = {'collection': 'orders'}
    timestamp = DateTimeField(default=datetime.datetime.utcnow)
    sales_items = ListField(DictField())
    total_price = IntField(min_value=0)


class Employment(EmbeddedDocument):
    meta = {'collection': 'employment'}


class Comment(EmbeddedDocument):
    meta = {'collection': 'comments'}
    timestamp = DateTimeField(default=datetime.datetime.utcnow)
    text = StringField(max_length=300)


class Location(Document):
    meta = {'collection': 'locations'}
    currency = StringField(max_length=3)
    country = StringField(max_length=3)


class Employee(Document):
    meta = {'collection': 'employees'}
    first_name = StringField()
    last_name = StringField()
    address = StringField()
    comments = EmbeddedDocumentListField(Comment)
    employment_history = EmbeddedDocumentListField(Employment)
    location = ReferenceField(Location)








