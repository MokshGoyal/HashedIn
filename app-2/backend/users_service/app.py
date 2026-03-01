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
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Prometheus Metrics
REQ_COUNT = Counter('users_request_count', 'Request Count', ['method', 'endpoint', 'http_status'])
REQ_LATENCY = Histogram('users_request_latency_seconds', 'Request Latency', ['endpoint'])

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
        
        logger.info("Users request processed", extra={
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

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email, 'role': self.role}

with app.app_context():
    db.create_all()

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    data = request.get_json()
    if 'name' in data: user.name = data['name']
    if 'email' in data: user.email = data['email']
    if 'role' in data: user.role = data['role']
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
