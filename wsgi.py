from app.factory import create_app
from app.db import setup_mongo

import os
import configparser


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

app = create_app()

app.config['DEBUG'] = config['SETTINGS']['DEBUG']
app.config['MONGO_URI'] = config['DATABASE']['MONGO_URI']

with app.app_context():
    setup_mongo(app)