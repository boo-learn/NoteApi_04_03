from api import app, multi_auth, request, db
from api.models.note import NoteModel
from api.models.user import UserModel
from api.models.tag import TagModel
from api.schemas.note import NoteSchema, NoteRequestSchema, note_schema, notes_schema
from utility.helpers import get_object_or_404
from flask_apispec import doc, marshal_with, use_kwargs
from webargs import fields


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

# /notes
# /notes?private=false
# /notes?private=false&username=admin
# /notes?private=false&username=user1

@app.route("/notes", methods=["GET"])
@doc(summary='Get all note', tags=['Notes'])
@doc(security=[{"basicAuth": []}])
@marshal_with(NoteSchema(many=True), code=200)
@multi_auth.login_required
def get_notes():
    # TODO: авторизованный пользователь получает только свои заметки и публичные заметки других пользователей
    user = multi_auth.current_user()
    notes = NoteModel.query.filter_by(is_archive=False)
    return notes, 200


# @app.route("/notes/public", methods=["GET"])
# @doc(summary='Get all public notes', tags=['Notes'])
# @marshal_with(NoteSchema(many=True), code=200)
# def get_public_notes():
#     notes = NoteModel.query.filter_by(private=False)
#     return notes, 200


# @app.route("/notes/public/filter", methods=["GET"])
# @doc(summary='Get all public notes by username', tags=['Notes'])
# @use_kwargs({"username": fields.Str()}, location='query')
# @marshal_with(NoteSchema(many=True), code=200)
# def get_public_notes_by_username(**kwargs):
#     username = kwargs["username"]
#     notes = NoteModel.query.join(NoteModel.author) \
#         .filter(UserModel.username == username) \
#         .filter(NoteModel.private == False).all()
#     return notes, 200


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


@app.route("/notes/<int:note_id>/add_tags", methods=["PUT"])
@doc(summary="Set tags to Note", tags=['Notes'])
@use_kwargs({"tags_id": fields.List(fields.Int())}, location='json')
@marshal_with(NoteSchema, code=200)
def note_add_tags(note_id, **kwargs):
    note = get_object_or_404(NoteModel, note_id)
    for tag_id in kwargs["tags_id"]:
        tag = TagModel.query.get(tag_id)
        note.tags.append(tag)
    db.session.commit()
    return note, 200


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
@doc(summary="Delete note", tags=['Notes'])
@doc(security=[{"basicAuth": []}])
@multi_auth.login_required
def delete_note(note_id):
    # TODO: Пользователь может удалять ТОЛЬКО свои заметки.
    #  Попытка удалить чужую заметку, возвращает ответ с кодом 403
    note = get_object_or_404(NoteModel, note_id)
    note.delete()
    return "", 204


# ?tag=<tag_name>
@app.route("/notes/filter", methods=["GET"])
@doc(summary='Get notes by tag name', tags=['Notes'])
@doc(security=[{"basicAuth": []}])
@use_kwargs({"tag": fields.Str()}, location='query')
@marshal_with(NoteSchema(many=True), code=200)
@multi_auth.login_required
def get_notes_by_tag_name(**kwargs):
    user = multi_auth.current_user()
    tag_name = kwargs["tag"]
    notes = NoteModel.query.join(NoteModel.tags).join(NoteModel.author) \
        .filter(UserModel.id == user.id) \
        .filter(TagModel.name == tag_name).all()
    return notes, 200


@doc(summary='Change importance for note', tags=['Notes'])
@app.route("/notes/<int:note_id>/change_importance", methods=["PUT"])
@marshal_with(NoteSchema, code=200)
# @multi_auth.login_required
def change_importance(note_id):
    # author = multi_auth.current_user()
    note = get_object_or_404(NoteModel, note_id)
    note.importance += 1
    if note.importance > 3:
        note.importance = 1
    note.save()
    return note, 200
