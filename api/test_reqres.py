from jsonschema import validate
import requests
from api.schemas import get_users, get_single_user, post_user, put_user, register_unsuccessful

endpoint = 'api/users/'
endpoint_register = 'api/register'

def test_all_users_should_have_email_field(url, headers):
    response = requests.get(f'{url}{endpoint}', headers=headers)
    body = response.json()
    emails = [element['email'] for element in body['data']]

    assert response.status_code == 200
    assert all('@' in email for email in emails)
    validate(body, schema=get_users)

def test_get_user_by_id(url, headers):
    id = '6'
    response = requests.get(f'{url}{endpoint}{id}', headers=headers)
    body = response.json()

    assert response.status_code == 200
    assert body['data']['id'] == int(id)
    validate(body, schema=get_single_user)


def test_get_user_by_id_not_found(url, headers):
    id = '13'
    response = requests.get(f'{url}{endpoint}{id}', headers=headers)
    body = response.json()

    assert response.status_code == 404
    assert body == {}


def test_create_user_should_return_id(url, headers):
    name = 'Mr. Proper'
    job = 'Cleaner'
    payload = {'name': name, 'job': job}
    response = requests.post((f'{url}{endpoint}'), json=payload, headers=headers)
    body = response.json()

    assert response.status_code == 201
    assert 'id' in body
    validate(body, schema=post_user)


def test_update_user_successful(url, headers):
    name = 'Bond'
    job = 'James'
    id = '2'
    payload = {'name': name, 'job': job}
    response = requests.put(f'{url}{endpoint}{id}', json=payload, headers=headers)
    body = response.json()

    assert response.status_code == 200
    assert body['name'] == name
    assert body['job'] == job
    validate(body, schema=put_user)


def test_delete_user(url, headers):
    id = '2'
    response = requests.delete(f'{url}{endpoint}{id}', headers=headers)
    assert response.status_code == 204
    assert response.text == ''


def test_register_unsuccessful(url, headers):

    payload = {
        "email": "mr@proper"
    }
    response = requests.post((f'{url}{endpoint_register}'),json=payload, headers=headers)
    body = response.json()

    assert response.status_code == 400
    validate(body, schema=register_unsuccessful)




