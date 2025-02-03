from fastapi import status


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        json={'title': 'Test', 'description': 'Test', 'state': 'todo'},
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data == {
        'title': 'Test',
        'description': 'Test',
        'state': 'todo',
        'id': 1,
    }
