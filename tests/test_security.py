def test_create_security_record(client, token):
    response = client.post('/security', json={'name': 'test_record'}, headers={'Authorization': token})
    assert response.status_code == 201
    assert 'id' in response.get_json()

def test_get_security_record(client, token):
    response = client.post('/security', json={'name': 'test_record'}, headers={'Authorization': token})
    record_id = response.get_json()['id']
    response = client.get(f'/security/{record_id}', headers={'Authorization': token})
    assert response.status_code == 200
    assert response.get_json()['id'] == record_id

def test_update_security_record(client, token):
    response = client.post('/security', json={'name': 'test_record'}, headers={'Authorization': token})
    record_id = response.get_json()['id']
    response = client.put(f'/security/{record_id}', json={'name': 'updated_record'}, headers={'Authorization': token})
    assert response.status_code == 200
    assert response.get_json()['name'] == 'updated_record'

def test_delete_security_record(client, token):
    response = client.post('/security', json={'name': 'test_record'}, headers={'Authorization': token})
    record_id = response.get_json()['id']
    response = client.delete(f'/security/{record_id}', headers={'Authorization': token})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Record deleted'

def test_list_security_records(client, token):
    client.post('/security', json={'name': 'record_1'}, headers={'Authorization': token})
    client.post('/security', json={'name': 'record_2'}, headers={'Authorization': token})
    response = client.get('/security', headers={'Authorization': token})
    assert response.status_code == 200
    assert len(response.get_json()) >= 2
