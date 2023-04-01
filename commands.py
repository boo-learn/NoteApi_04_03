from api import app
from api.models.user import UserModel
import click


@app.cli.command('createsuperuser')
def create_superuser():
    """
    Creates a user with the admin role
    """
    username = input("Username[default 'admin']:")
    password = input("Password[default 'admin']:")
    user = UserModel(username, password, role="admin")
    user.save()
    print(f"Superuser create successful! id={user.id}")


@click.argument('role', default="simple_user")
@app.cli.command('all-users')
def get_all_users(role):
    users = UserModel.query.filter_by(role=role)
    for num, user in enumerate(users, 1):
        print(f"{num}. {user.username}")