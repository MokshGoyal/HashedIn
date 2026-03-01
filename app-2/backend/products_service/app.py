from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
import os
import time
import logging
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, Histogram, generate_latest
from opentelemetry import trace

# Set up JSON structured logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(trace_id)s %(message)s')
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)

app = Flask(__name__)
# Use SQLite for simple local testing; wait for DB URI from env
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///products.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Prometheus Metrics
REQ_COUNT = Counter('products_request_count', 'Request Count', ['method', 'endpoint', 'http_status'])
REQ_LATENCY = Histogram('products_request_latency_seconds', 'Request Latency', ['endpoint'])

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    resp_time = time.time() - request.start_time
    if request.path != '/metrics' and request.path != '/health':
        REQ_COUNT.labels(request.method, request.path, response.status_code).inc()
        REQ_LATENCY.labels(request.path).observe(resp_time)
        
        # Inject OTel Trace ID into JSON logs
        span = trace.get_current_span()
        trace_id = format(span.get_span_context().trace_id, "032x") if span.is_recording() else ""
        
        logger.info("Products request processed", extra={
            "http_method": request.method,
            "http_path": request.path,
            "status_code": response.status_code,
            "response_time": resp_time,
            "trace_id": trace_id
        })
    return response

@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype='text/plain')

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'price': self.price, 'category': self.category}

with app.app_context():
    db.create_all()

@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])

@app.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    new_product = Product(name=data['name'], price=data['price'], category=data['category'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@app.route('/products/<int:prod_id>', methods=['GET'])
def get_product(prod_id):
    product = db.session.get(Product, prod_id)
    if product:
        return jsonify(product.to_dict())
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products/<int:prod_id>', methods=['PUT'])
def update_product(prod_id):
    product = db.session.get(Product, prod_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    data = request.get_json()
    if 'name' in data: product.name = data['name']
    if 'price' in data: product.price = data['price']
    if 'category' in data: product.category = data['category']
    db.session.commit()
    return jsonify(product.to_dict())

@app.route('/products/<int:prod_id>', methods=['DELETE'])
def delete_product(prod_id):
    product = db.session.get(Product, prod_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
