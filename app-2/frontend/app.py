from flask import Flask, render_template, request, jsonify, Response
import requests
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

# Prometheus Metrics
REQ_COUNT = Counter('frontend_request_count', 'Request Count', ['method', 'endpoint', 'http_status'])
REQ_LATENCY = Histogram('frontend_request_latency_seconds', 'Request Latency', ['endpoint'])

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
        
        logger.info("Frontend request processed", extra={
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

USERS_URL = os.environ.get('USERS_SERVICE_URL', 'http://localhost:5001')
PRODUCTS_URL = os.environ.get('PRODUCTS_SERVICE_URL', 'http://localhost:5002')
ORDERS_URL = os.environ.get('ORDERS_SERVICE_URL', 'http://localhost:5003')

@app.route('/')
def index():
    return render_template('index.html')

# API Gateways / Proxies
@app.route('/api/<service>/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def proxy(service, path):
    if service == 'users':
        base_url = USERS_URL
    elif service == 'products':
        base_url = PRODUCTS_URL
    elif service == 'orders':
        base_url = ORDERS_URL
    else:
        return jsonify({'error': 'Service not found'}), 404

    url = f"{base_url}/{path}"
    
    try:
        if request.method == 'GET':
            resp = requests.get(url, params=request.args)
        elif request.method == 'POST':
            resp = requests.post(url, json=request.get_json())
        elif request.method == 'PUT':
            resp = requests.put(url, json=request.get_json())
        elif request.method == 'PATCH':
            resp = requests.patch(url, json=request.get_json())
        elif request.method == 'DELETE':
            resp = requests.delete(url)
            
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.headers.items() if name.lower() not in excluded_headers]
        
        return Response(resp.content, resp.status_code, headers)
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 502

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
