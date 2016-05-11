import pytest


def test_get_todos_successful(logged_client, todos):
    result = logged_client.get('/todos')
    assert result.status_code == 200
    assert result.json == [
        {'id': 1, 'text': 'Test1', 'completed': False, 'completed_on': None},
        {'id': 2, 'text': 'Test2', 'completed': True, 'completed_on': None}]


def test_get_todos_filtered_successful(logged_client, todos):
    result = logged_client.get('/todos', query_string={'completed': True})
    assert result.status_code == 200
    assert result.json == [
        {'id': 2, 'text': 'Test2', 'completed': True, 'completed_on': None}]


@pytest.mark.parametrize("test_data, expected", [
    ({'completed': 10}, 422),
    ({'completed': 'random'}, 422),
    ({'completed': 'true'}, 200),
    ({'garbage': 'True'}, 200),
    ({'user': 123}, 200),
])
def test_get_todos_filtered_invalid_query(logged_client, test_data, expected):
    result = logged_client.get('/todos', query_string=test_data)
    assert result.status_code == expected


def test_get_todo_successful(logged_client, todos):
    result = logged_client.get('/todos/1')
    assert result.status_code == 200
    assert result.json == {
        'id': 1, 'text': 'Test1', 'completed': False, 'completed_on': None}


def test_post_todo_successful(logged_client):
    data = {'text': 'Test1', 'completed': False}
    result = logged_client.post('/todos', json=data)
    assert result.status_code == 201
    assert result.json == {
        'id': 1, 'text': 'Test1', 'completed': False, 'completed_on': None}
    assert logged_client.get('/todos/1').status_code == 200


@pytest.mark.parametrize("test_data, expected", [
    ({'complete': True}, 422),
    ({'garbage': ''}, 422),
    ({'text': 1}, 422),
])
def test_post_todo_invalid_data(logged_client, test_data, expected):
    result = logged_client.post('/todos', json=test_data)
    assert result.status_code == expected


def test_delete_todo_successful(logged_client, todos):
    _id = todos[0].id
    result = logged_client.delete('/todos/{}'.format(_id))
    assert result.status_code == 200
    assert result.json == {'message': 'Todo {} deleted'.format(_id)}
    assert logged_client.get('/todos/{}'.format(_id)).status_code == 404


def test_put_todo_successful(logged_client, todos):
    data = {'text': 'Updated test1', 'completed': True}
    _id = todos[0].id
    result = logged_client.put('/todos/{}'.format(_id), json=data)
    assert result.status_code == 200
    assert result.json == {
        'id': _id, 'text': data['text'], 'completed': data['completed'],
        'completed_on': None}
