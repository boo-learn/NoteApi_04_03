from api import app, docs
from config import Config
from api.handlers import auth, note, user, tag

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

# TAGS
docs.register(tag.get_tag_by_id)
docs.register(tag.get_tags)
docs.register(tag.create_tag)

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
