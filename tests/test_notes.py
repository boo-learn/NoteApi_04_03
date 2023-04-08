import pytest
from tests.init_test import client, application, auth_headers
from api.models.user import UserModel
from api.models.note import NoteModel


@pytest.fixture()
def user():
    user_data = {"username": "testuser", "password": "1234"}
    user = UserModel(**user_data)
    user.save()
    return user


@pytest.fixture()
def note(user):
    note_data = {"author_id": user.id, "text": "Quote for testuser", "private": False}
    note = NoteModel(**note_data)
    note.save()
    return note


@pytest.fixture()
def user_admin():
    user_data = {"username": "admin", "password": "admin"}
    user = UserModel(**user_data)
    user.save()
    return user


@pytest.fixture()
def note_admin(user_admin):
    note_data = {"author_id": user_admin.id, "text": "Quote for admin"}
    note = NoteModel(**note_data)
    note.save()
    return note


@pytest.fixture()
def notes(user_admin, user):
    notes_data = [
        {"author_id": user_admin.id, "text": "Note-1", "private": False},
        {"author_id": user_admin.id, "text": "Note-2", "private": False},
        {"author_id": user_admin.id, "text": "Note-3", "private": True},
        {"author_id": user.id, "text": "Note-4", "private": True},
        {"author_id": user.id, "text": "Note-5", "private": False},
    ]
    _notes = []
    for note_data in notes_data:
        note = NoteModel(**note_data)
        note.save()
        _notes.append(note)

    return _notes


def test_note_get_by_id(client, note, auth_headers):
    response = client.get('/notes/1', headers=auth_headers)
    assert response.status_code == 200
    assert response.json["text"] == note.text


def test_note_not_found(client, note, auth_headers):
    response = client.get('/notes/2', headers=auth_headers)
    assert response.status_code == 404


def test_note_creation(client, auth_headers):
    note_data = {
        "text": "Quote for auth user",
        "private": False
    }
    response = client.post('/notes',
                           json=note_data,
                           headers=auth_headers,
                           )
    data = response.json
    assert response.status_code == 201
    assert note_data["text"] == data["text"]
    assert note_data["private"] == data["private"]


def test_note_edit(client, note_admin, auth_headers):
    note_edit_data = {
        "text": "Edited note"
    }
    response = client.put(f'/notes/{note_admin.id}',
                          json=note_edit_data,
                          headers=auth_headers,
                          )
    data = response.json
    assert response.status_code == 200
    assert data["text"] == note_edit_data["text"]


@pytest.mark.skip(reason="test not implemented")
def test_note_delete(client, auth_headers):
    pass
    # TODO: реализуйте тест на удаление заметки и запустите его, убрав декоратор @pytest.mark.skip


def test_get_public_notes(client, notes):
    response = client.get(f'/notes/public')
    data = response.json
    assert response.status_code == 200
    assert len(data) == 3
    assert data[0]["text"] == "Note-1"
    assert data[1]["text"] == "Note-2"


def test_get_public_notes_by_username(client, notes):
    response = client.get(f'/notes/public/filter?username=admin')
    data = response.json
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["text"] == "Note-1"
    assert data[1]["text"] == "Note-2"
