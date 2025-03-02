# import uuid
# from io import BytesIO
# from PIL import Image
# import requests

# @celery.task
# def process_images(request_id):
#     products = list(mongo.db.products.find({'request_id': request_id}))
#     for product in products:
#         input_urls = product['input_image_urls']
#         output_urls = []
#         for url in input_urls:
#             response = requests.get(url.strip())
#             img = Image.open(BytesIO(response.content))
#             img = img.convert("RGB")
#             output = BytesIO()
#             img.save(output, format='JPEG', quality=50)
#             # upload to cloud storage
#             # 
#             output_url = f"https://example.com/output/{uuid.uuid4()}.jpg"  # Replace with actual storage logic
#             output_urls.append(output_url)
#         mongo.db.products.update_one(
#             {'_id': product['_id']},
#             {'$set': {'output_image_urls': output_urls, 'status': 'processed'}}
#         )

#     mongo.db.processing_requests.update_one(
#         {'request_id': request_id},
#         {'$set': {'status': 'completed'}}
#     )