import os

os.environ["DATABASE_URI"] = f"sqlite:///'test.db'"

import pytest
from api import db
from app import app
from api.models.user import UserModel


@pytest.fixture()
def application():
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture()
def client(application):
    return application.test_client()


def test_user_get_by_id(client):
    user_create = {
        "username": "admin",
        "password": "admin"
    }
    user_data = {
        "id": 1,
        "username": "admin"
    }
    user = UserModel(**user_create)
    user.save()
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json == user_data


def test_user_edit(client):
    user_create = {
        "username": "admin",
        "password": "admin"
    }
    edit_user = {"username": "new_user"}
    user = UserModel(**user_create)
    user.save()
    response = client.put('/users/1',
               json=edit_user,
               content_type='application/json')
    assert response.status_code == 200
    user = UserModel.query.get(1)
    assert user.username == edit_user["username"]