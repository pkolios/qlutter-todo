import pytest


def test_register_successfull(client):
    data = {'email': 'test_register@example.org', 'password': 'sikret'}
    result = client.post('/register', json=data)
    assert result.status_code == 201
    assert result.json['email'] == data['email']


@pytest.mark.parametrize("test_data, expected", [
    ({'email': 'test_register@example.org'}, 422),
    ({'password': 'sikret'}, 422),
    ({'email': 'bad_format', 'password': 'sikret'}, 422),
])
def test_register_invalid_data(client, test_data, expected):
    result = client.post('/register', json=test_data)
    assert result.status_code == expected


def test_auth_successful(client, user):
    email, password = user
    data = {'email': email, 'password': password}
    result = client.post('/auth', json=data)
    assert result.status_code == 200
    assert 'access_token' in result.json
    assert len(result.json['access_token']) != 0


@pytest.mark.parametrize("test_data, expected", [
    ({'email': 'wrong@example.org', 'password': ''}, 401),
    ({'email': 'test_register@example.org'}, 401),
    ({'password': 'sikret'}, 401),
    ({'email': 'bad_format', 'password': 'sikret'}, 401),
])
def test_auth_invalid_credentials(client, test_data, expected):
    result = client.post('/auth', json=test_data)
    assert result.status_code == expected


def test_logout_successful(client, user):
    email, password = user
    data = {'email': email, 'password': password}
    access_token = client.post('/auth', json=data).json.get('access_token')
    headers = {'Authorization': 'JWT {}'.format(access_token)}
    result = client.post('/logout', headers=headers)
    assert result.status_code == 200
