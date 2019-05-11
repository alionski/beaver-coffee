from flask import Flask
from flask_mongoengine import MongoEngine
import configparser

app = Flask(__name__)

# there should be the file called credentials.ini in the same dir
# see credentials_example.ini
# do not add credentials.ini to git (!)
config = configparser.ConfigParser()
config.read('app/credentials.ini')
username = config['mongo_atlas']['username']
password = config['mongo_atlas']['password']
atlas_uri = "mongodb+srv://" + username + ":" + password + "@cluster0-jwmsg.mongodb.net/beaver?retryWrites=true"

# Settings used by MongoEngine
app.config['MONGODB_SETTINGS'] = {
    'db': 'beaver',
    'host': atlas_uri,
    'connect': False
}

db = MongoEngine(app)

from app import routes, models


