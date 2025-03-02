from app.factory import create_app
from app.db import setup_mongo

import os
import configparser


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))

if __name__ == "__main__":
    app = create_app()
    app.config['DEBUG'] = True
    app.config['MONGO_URI'] = config['DATABASE']['MONGO_URI']
    # app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
    # app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

    # print(app.config['MONGO_URI'])

    # init_db(app)

    with app.app_context():
        setup_mongo(app)
        app.run()