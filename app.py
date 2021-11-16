"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "shilohiscute"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home():
    """shows list of all the users in the database"""

    return redirect('/users')

@app.route('/users')
def list_users():
    """shows list of all the users in the database,
    clicking on user will direct them to the details page
    for that user"""
    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('users.html', users=users)

@app.route('/users/new')
def display_form():
    """displays form to add new user to databses"""

    return render_template('form.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    """adds new user to database then redirects to list of all users"""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form["img-url"]

    new_user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/<int:user_id>')
def display_user(user_id):
    """shows details about the specified user"""

    user = User.query.get_or_404(user_id)
    return render_template('details.html', user=user)

@app.route('/user/<int:user_id>/edit')
def edit_user(user_id):
    """shows edit page for a user"""

    user = User.query.get_or_404(user_id)

    return render_template('edit.html', user=user)

@app.route('/user/<int:user_id>/edit', methods=["POST"])
def post_edit_user(user_id):

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.img_url = request.form["img-url"]

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/user/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """deletes existing user from database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

    


