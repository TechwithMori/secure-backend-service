from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import requests
from functools import wraps
import logging
from datetime import datetime

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///security.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define the SecurityRecord model
class SecurityRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    description = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Define a token_required decorator for securing routes
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            response = requests.post('http://auth-service:5001/auth/validate', json={'token': token})
            response.raise_for_status()
            if response.status_code != 200:
                app.logger.debug(f"Token validation failed: {response.status_code}, {response.text}")
                return jsonify({'message': 'Invalid token!'}), 403
        except requests.exceptions.RequestException as e:
            app.logger.debug(f"Authorization service error: {str(e)}")
            return jsonify({'message': 'Authorization service not available'}), 503
        return f(*args, **kwargs)
    return decorated_function

# Define routes
@app.route('/security', methods=['POST'], endpoint='create_security_record')
@token_required
def create_security_record():
    data = request.get_json()
    if not data or not 'name' in data:
        return jsonify({'message': 'Invalid input'}), 400
    new_record = SecurityRecord(name=data['name'], description=data.get('description'))
    db.session.add(new_record)
    db.session.commit()
    return jsonify({'id': new_record.id}), 201

@app.route('/security/<int:id>', methods=['GET'], endpoint='get_security_record')
@token_required
def get_security_record(id):
    record = SecurityRecord.query.get_or_404(id)
    return jsonify({'id': record.id, 'name': record.name, 'description': record.description, 'timestamp': record.timestamp})

@app.route('/security/<int:id>', methods=['PUT'], endpoint='update_security_record')
@token_required
def update_security_record(id):
    data = request.get_json()
    record = SecurityRecord.query.get_or_404(id)
    if not data:
        return jsonify({'message': 'Invalid input'}), 400
    record.name = data.get('name', record.name)
    record.description = data.get('description', record.description)
    db.session.commit()
    return jsonify({'id': record.id, 'name': record.name, 'description': record.description, 'timestamp': record.timestamp})

@app.route('/security/<int:id>', methods=['DELETE'], endpoint='delete_security_record')
@token_required
def delete_security_record(id):
    record = SecurityRecord.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted'})

@app.route('/security', methods=['GET'], endpoint='list_security_records')
@token_required
def list_security_records():
    records = SecurityRecord.query.all()
    output = []
    for record in records:
        record_data = {'id': record.id, 'name': record.name, 'description': record.description, 'timestamp': record.timestamp}
        output.append(record_data)
    return jsonify(output)

# Define error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'message': 'Bad request'}), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({'message': 'Internal server error'}), 500

# Run the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
