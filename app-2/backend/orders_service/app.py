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
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///orders.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Prometheus Metrics
REQ_COUNT = Counter('orders_request_count', 'Request Count', ['method', 'endpoint', 'http_status'])
REQ_LATENCY = Histogram('orders_request_latency_seconds', 'Request Latency', ['endpoint'])

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
        
        logger.info("Orders request processed", extra={
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

class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id, 'product_id': self.product_id, 'quantity': self.quantity, 'status': self.status}

with app.app_context():
    db.create_all()

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([o.to_dict() for o in orders])

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(user_id=data['user_id'], product_id=data['product_id'], quantity=data['quantity'], status=data.get('status', 'Pending'))
    db.session.add(new_order)
    db.session.commit()
    return jsonify(new_order.to_dict()), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = db.session.get(Order, order_id)
    if order:
        return jsonify(order.to_dict())
    return jsonify({'error': 'Order not found'}), 404

@app.route('/orders/<int:order_id>', methods=['PUT', 'PATCH'])
def update_order(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    data = request.get_json()
    if 'user_id' in data: order.user_id = data['user_id']
    if 'product_id' in data: order.product_id = data['product_id']
    if 'quantity' in data: order.quantity = data['quantity']
    if 'status' in data: order.status = data['status']
    db.session.commit()
    return jsonify(order.to_dict())

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = db.session.get(Order, order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'Order deleted'}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
