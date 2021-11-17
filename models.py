"""Models for Blogly."""

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.schema import ForeignKey

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User class: includes first name, last name and a profile image"""
    __tablename__ = 'users'

    @property
    def get_full_name(self):
        """returns user's full name"""

        return f"{self.first_name} {self.last_name}"

    id = db.Column(
        db.Integer, 
        primary_key = True, 
        autoincrement = True
    )

    first_name = db.Column(
        db.String(15), 
        nullable = False
    )

    last_name = db.Column(
        db.String(15),
        nullable = False
    )

    img_url = db.Column(
        db.Text,
        nullable = False
    )

class Post(db.Model):
    """class for a user's post: includes title, content and time created"""

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key = True,
        autoincrement = True
    )

    title = db.Column(
        db.String(25),
        nullable = False
    )

    content = db.Column(
        db.Text,
        nullable = False
    )

    created_at = db.Column(
        db.DateTime,
        default = date.today,
        nullable = False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id')
    )

    user = db.relationship('User', backref='posts')
