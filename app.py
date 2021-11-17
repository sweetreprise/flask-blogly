"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

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

    return render_template('users-list.html', users=users)

@app.route('/users/new')
def show_user_form():
    """displays form to add new user to databses"""

    return render_template('user-form.html')

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
    posts = Post.query.filter_by(user_id=user_id).all()
    
    return render_template('user-details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """shows edit page for a user"""

    user = User.query.get_or_404(user_id)

    return render_template('edit-user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def handle_edit_user(user_id):
    """allows user to edit user info"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.img_url = request.form["img-url"]

    db.session.add(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """deletes existing user from database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

# Part 2

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """shows form to add a post for that user"""

    user = User.query.get_or_404(user_id)

    return render_template('post-form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_post(user_id):
    """adds new post for that user"""

    user = User.query.get_or_404(user_id)

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user.id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """displays post depending on post id"""

    post = Post.query.get_or_404(post_id)

    return render_template('post-details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """shows form to edit a post"""

    post = Post.query.get_or_404(post_id)

    return render_template('edit-post.html', post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_edit_post(post_id):
    """handles form submission for post edits"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """deletes post from that user"""

    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect('/users')




    


