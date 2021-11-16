"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
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
