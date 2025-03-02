from flask import current_app as app

from app.factory import mongo


def create_processing_request(processing_request):
    mongo.db.processing_requests.insert_one(processing_request)

def create_products(products):
    mongo.db.products.insert_many(products)

def find_processing_request(request_id):
    return mongo.db.processing_requests.find_one({'request_id': request_id})

def find_all_products(request_id):
    return list(mongo.db.products.find({'request_id': request_id}))
    