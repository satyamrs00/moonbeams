import uuid
from io import BytesIO
from PIL import Image
import requests
from app import db
from app.helpers import cloudinary_helper

def process_images(request_id):
    products = db.find_all_products(request_id)
    for product in products:
        input_urls = product['input_image_urls']
        output_urls = []
        for i in range (len(input_urls)):
            url = input_urls[i]
            response = requests.get(url.strip())
            img = Image.open(BytesIO(response.content))
            img = img.convert("RGB")
            output = BytesIO()
            img.save(output, format='JPEG', quality=50)

            output_url = cloudinary_helper.upload_image(output.getvalue(), str(product['_id']) + str(i))
            output_urls.append(output_url)

        db.update_product(product['_id'], output_urls)
    db.update_processing_request(request_id)

    