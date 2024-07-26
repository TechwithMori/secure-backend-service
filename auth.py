from flask import Flask, request, jsonify
import uuid

auth_app = Flask(__name__)

# Simulated in-memory store for tokens
valid_tokens = {}

@auth_app.route('/auth/token', methods=['POST'])
def get_token():
    # Simulate token creation
    user_id = request.json.get('user_id')
    if user_id:
        token = str(uuid.uuid4())
        valid_tokens[token] = user_id
        return jsonify({'token': token}), 201
    return jsonify({'message': 'User ID required'}), 400

@auth_app.route('/auth/validate', methods=['POST'])
def validate_token():
    token = request.json.get('token')
    if token in valid_tokens:
        return jsonify({'valid': True}), 200
    return jsonify({'valid': False}), 401

if __name__ == '__main__':
    auth_app.run(host='0.0.0.0', port=5001)