from flask import Blueprint, request, jsonify
from flask_cors import CORS
from io import StringIO
import uuid
import csv
from datetime import datetime
from app import db
from app.helpers import process_helper
from threading import Thread

csv_processor_v1 = Blueprint(
    'csv_processor_v1', 'csv_processor_v1', url_prefix='/csv')

CORS(csv_processor_v1)

@csv_processor_v1.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400

    # Validate and process CSV file
    request_id = str(uuid.uuid4())
    csv_data = file.read().decode('utf-8')
    csv_reader = csv.reader(StringIO(csv_data), delimiter=',')
    next(csv_reader)

    products = []
    for row in csv_reader:
        if len(row) != 3:
            return jsonify({'error': 'Invalid CSV file'}), 400

        serial_number, product_name, input_image_urls = row
        product = {
            'request_id': request_id,
            'serial_number': int(serial_number),
            'product_name': product_name,
            'input_image_urls': input_image_urls.split(','),
            'output_image_urls': [],
            'status': 'pending'
        }
        products.append(product)

    processing_request = {
        'request_id': request_id,
        'status': 'pending',
        'created_at': datetime.now(),
    }
    
    db.create_processing_request(processing_request)
    db.create_products(products)

    # run process images task on new thread
    thread = Thread(target=process_helper.process_images, args=(request_id,))
    thread.start()    

    return jsonify({'request_id': request_id})


@csv_processor_v1.route('/status/<request_id>', methods=['GET'])
def check_status(request_id):
    request = db.find_processing_request(request_id)
    if not request:
        return jsonify({'error': 'Invalid request ID'}), 404

    products = db.find_all_products(request_id)
    products_data = [
        {
            'serial_number': product['serial_number'],
            'product_name': product['product_name'],
            'input_image_urls': product['input_image_urls'],
            'output_image_urls': product['output_image_urls'],
            'status': product['status']
        }
        for product in products
    ]

    return jsonify({
        'request_id': request_id,
        'status': request['status'],
        'products': products_data
    })


@csv_processor_v1.route('/output/<request_id>', methods=['GET'])
def download_output(request_id):
    request = db.find_processing_request(request_id)
    if not request:
        return jsonify({'error': 'Invalid request ID'}), 404
    
    if request['status'] != 'completed':
        return jsonify({'error': 'Request is not completed yet'}), 400
    
    products = db.find_all_products(request_id)
    data = [
        ['serial_number', 'product_name', 'input_image_urls', 'output_image_urls']
    ]
    for product in products:
        data.append([
            product['serial_number'],
            product['product_name'],
            ','.join(product['input_image_urls']),
            ','.join(product['output_image_urls'])
        ])
    
    output = StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerows(data)
    output.seek(0)

    return output.getvalue(), 200, {
        'Content-Type': 'text/csv',
        'Content-Disposition': f'attachment; filename={request_id}.csv'
    }
