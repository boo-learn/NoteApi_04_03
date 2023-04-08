from api import app, docs
from config import Config
from api.handlers import auth, note, user, tag, file

# CRUD

# Create --> POST
# Read --> GET
# Update --> PUT
# Delete --> DELETE

# USERS
docs.register(user.get_user_by_id)
docs.register(user.create_user)
docs.register(user.get_users)

# NOTES
docs.register(note.get_note_by_id)
docs.register(note.get_notes)
docs.register(note.create_note)
docs.register(note.note_add_tags)
docs.register(note.get_notes_by_tag_name)
docs.register(note.delete_note)

# TAGS
docs.register(tag.get_tag_by_id)
docs.register(tag.get_tags)
docs.register(tag.create_tag)

# UPLOAD
docs.register(file.upload_file)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
