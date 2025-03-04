import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db
import pytest

@pytest.fixture(scope='module')
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        db.create_all()
    
    yield client

    with app.app_context():
        db.drop_all()
