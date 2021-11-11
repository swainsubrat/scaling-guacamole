# pylint: disable=no-member
# pylint: disable=too-few-public-methods
"""
Models for home component

superuser = User(name="admin", username="admin", email="admin@swinder.com", password="admin1234", privilage="superuser")

"""
from swinder import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    """
    To load the current user
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    The User table in which the user data is stored
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    privilage = db.Column(db.String(20), nullable=False, default="user")

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.name}')"


db.create_all()
