from datetime import datetime

import factory
import factory.fuzzy
from fastapi import status

from fastapi_zero.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta:
        model = Todo

    title = factory.Faker('text', max_nb_chars=10)
    description = factory.Faker('text', max_nb_chars=30)
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1
    created_at = datetime.now()
    updated_at = datetime.now()


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        json={'title': 'Test', 'description': 'Test', 'state': 'todo'},
        headers={'Authorization': f'Bearer {token}'},
    )

    data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert data['title'] == 'Test'
    assert data['description'] == 'Test'
    assert data['state'] == 'todo'


def test_delete_todo_error(client, token):
    response = client.delete(
        '/todos/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}


def test_patch_todo_error(client, token):
    response = client.patch(
        '/todos/1', headers={'Authorization': f'Bearer {token}'}, json={}
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found'}
