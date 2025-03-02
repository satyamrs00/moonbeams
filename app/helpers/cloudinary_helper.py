from dotenv import load_dotenv
load_dotenv()

import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api

import json

config = cloudinary.config(secure=True)

def upload_image(image, id):
    cloudinary.uploader.upload(image, public_id=id, unique_filename = False, overwrite=True)

    srcURL = CloudinaryImage(id).build_url()
    return srcURL