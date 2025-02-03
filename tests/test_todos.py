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


def test_list_todos_should_return_5_todos(session, client, token, user):
    expected_todos = 5
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_pagination_should_return_2_todos(
    session, user, client, token
):
    expected_todos = 2
    session.bulk_save_objects(TodoFactory.create_batch(5, user_id=user.id))
    session.commit()

    response = client.get(
        '/todos/',  # /todos/?offset=0&limit=2
        headers={'Authorization': f'Bearer {token}'},
        params={'offset': 0, 'limit': 2},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_title_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, title='Test Title')
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        params={'title': 'Test'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_list_todos_filter_state_should_return_5_todos(
    session, user, client, token
):
    expected_todos = 5
    session.bulk_save_objects(
        TodoFactory.create_batch(5, user_id=user.id, state=TodoState.done)
    )
    session.commit()

    response = client.get(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        params={'state': 'done'},
    )

    assert len(response.json()['todos']) == expected_todos


def test_delete_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)
    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.delete(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'Todo deleted'}


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


def test_patch_todo(session, client, user, token):
    todo = TodoFactory(user_id=user.id)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    response = client.patch(
        f'/todos/{todo.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={'title': 'Updated title'},
    )

    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data == {
        'title': 'Updated title',
        'description': todo.description,
        'state': todo.state,
        'id': todo.id,
    }
