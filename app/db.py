from flask_pymongo import PyMongo

mongo = None

def setup_mongo(app):
    global mongo
    mongo = PyMongo(app)

def create_processing_request(processing_request):
    mongo.db.processing_requests.insert_one(processing_request)

def create_products(products):
    mongo.db.products.insert_many(products)

def find_processing_request(request_id):
    return mongo.db.processing_requests.find_one({'request_id': request_id})

def find_all_products(request_id):
    return list(mongo.db.products.find({'request_id': request_id}))
    
def update_product(_id, output_urls):
    mongo.db.products.update_one(
        {'_id': _id},
        {'$set': {'output_image_urls': output_urls, 'status': 'processed'}}
    )

def update_processing_request(request_id):
    mongo.db.processing_requests.update_one(
        {'request_id': request_id},
        {'$set': {'status': 'completed'}}
    )