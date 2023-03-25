from api import app, multi_auth, request
from api.models.note import NoteModel
from api.models.user import UserModel
from api.schemas.note import NoteSchema, NoteRequestSchema, note_schema, notes_schema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs


@app.route("/notes/<int:note_id>", methods=["GET"])
@doc(summary='Get note by id', tags=['Notes'])
@doc(security=[{"basicAuth": []}])
@marshal_with(NoteSchema, code=200)
@multi_auth.login_required
def get_note_by_id(note_id):
    # TODO(complete): авторизованный пользователь может получить только свою заметку или публичную заметку других пользователей
    #  Попытка получить чужую приватную заметку, возвращает ответ с кодом 403
    user = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    notes = NoteModel.query.join(NoteModel.author). \
        filter((UserModel.username == user.username) | (NoteModel.private == False)).all()
    if note in notes:
        return note, 200

    return "...", 403


@app.route("/notes", methods=["GET"])
@doc(summary='Get all note', tags=['Notes'])
@doc(security=[{"basicAuth": []}])
@marshal_with(NoteSchema(many=True), code=200)
@multi_auth.login_required
def get_notes():
    # TODO: авторизованный пользователь получает только свои заметки и публичные заметки других пользователей
    user = multi_auth.current_user()
    notes = NoteModel.query.all()
    return notes, 200


@app.route("/notes", methods=["POST"])
@doc(summary='Create new note', tags=['Notes'])
@doc(security=[{"basicAuth": []}])
@marshal_with(NoteSchema, code=201)
@use_kwargs(NoteRequestSchema, location='json')
@multi_auth.login_required
def create_note(**kwargs):
    user = multi_auth.current_user()
    # note_data = request.json
    note = NoteModel(author_id=user.id, **kwargs)
    note.save()
    return note, 201


@app.route("/notes/<int:note_id>", methods=["PUT"])
@multi_auth.login_required
def edit_note(note_id):
    # TODO: Пользователь может редактировать ТОЛЬКО свои заметки.
    #  Попытка редактировать чужую заметку, возвращает ответ с кодом 403
    author = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    note_data = request.json
    note.text = note_data["text"]
    note.private = note_data.get("private") or note.private
    note.save()
    return note_schema.dump(note), 200


@app.route("/notes/<int:note_id>", methods=["DELETE"])
@multi_auth.login_required
def delete_note(self, note_id):
    # TODO: Пользователь может удалять ТОЛЬКО свои заметки.
    #  Попытка удалить чужую заметку, возвращает ответ с кодом 403
    raise NotImplemented("Метод не реализован")
