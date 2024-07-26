import sys
import os
import pytest
from app import app, db

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

@pytest.fixture(scope='module')
def token(client):
    response = client.post('/auth/token', json={'user_id': 'test_user'})
    return response.get_json()['token']
