import pytest
from app import app, db
from models import KeyValue

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # in-memory DB for tests
    with app.app_context():
        db.create_all()
    
    with app.test_client() as client:
        yield client
    
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_set_and_get(client):
    response = client.post('/set', json={"key": "a", "value": "123"})
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}

    response = client.get('/get/a')
    assert response.status_code == 200
    assert response.get_json() == {"key": "a", "value": "123"}

    response = client.get('/get/nonexistent')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Key not found"}


def test_delete(client):
    client.post('/set', json={"key": "b", "value": "456"})
    
    response = client.delete('/delete/b')
    assert response.status_code == 200
    assert response.get_json() == {"status": "deleted"}

    response = client.delete('/delete/nonexistent')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Key not found"}

def test_transactions(client):
    response = client.post('/begin')
    assert response.status_code == 200
    assert response.get_json() == {"status": "transaction started"}

    response = client.post('/set', json={"key": "tx1", "value": "val1"})
    assert response.status_code == 200


    response = client.post('/rollback')
    assert response.status_code == 200
    assert response.get_json() == {"status": "transaction rolled back"}

    response = client.get('/get/tx1')
    assert response.status_code == 404

    client.post('/begin')
    client.post('/set', json={"key": "tx2", "value": "val2"})

    response = client.post('/commit')
    assert response.status_code == 200
    assert response.get_json() == {"status": "transaction committed"}

    response = client.get('/get/tx2')
    assert response.status_code == 200
    assert response.get_json() == {"key": "tx2", "value": "val2"}


def test_invalid_requests(client):

    response = client.post('/set', json={"value": "no_key"})
    assert response.status_code == 400

    response = client.post('/set', json={"key": "no_value"})
    assert response.status_code == 400

    response = client.post('/rollback')
    assert response.status_code == 400

    response = client.post('/commit')
    assert response.status_code == 400