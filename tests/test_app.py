from fastapi import status


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # act (ação)

    assert response.status_code == status.HTTP_200_OK  # assert (afirmação)
    assert response.json() == {
        'message': 'Hello, World!'
    }  # assert (afirmação)


def test_read_html_deve_retornar_ok_e_html(client):
    response = client.get('/html')

    assert response.status_code == status.HTTP_200_OK
    assert '<h1>Olá, Mundo!</h1>' in response.text


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'password': 'password',
            'email': 'test@test.com',
        },
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {
        'id': 1,
        'username': 'testusername',
        'email': 'test@test.com',
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'users': [
            {
                'id': 1,
                'username': 'testusername',
                'email': 'test@test.com',
            }
        ]
    }


def test_read_users_by_id(client):
    response = client.get('/users/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'id': 1,
        'username': 'testusername',
        'email': 'test@test.com',
    }


def test_read_users_by_id_not_fount(client):
    response = client.get('/users/13')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User with id 13 not found!'}


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'username': 'machadoah',
            'password': 'password',
            'email': 'antonio@email.com',
        },
    )

    assert response.json() == {
        'id': 1,
        'username': 'machadoah',
        'email': 'antonio@email.com',
    }


def test_update_user_not_exists(client):
    response = client.put(
        '/users/13',
        json={
            'username': 'machadoah',
            'password': 'password',
            'email': 'antonio@email.com',
        },
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': 'User with id 1 deleted!'}


def test_delete_user_not_exists(client):
    response = client.delete('/users/80')

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'User not found!'}
