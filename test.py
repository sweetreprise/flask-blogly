from unittest import TestCase
from app import app
from models import db, User, Post

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# db.drop_all()
# db.create_all()

class UserTests(TestCase):

    def setUp(self):
        """things to run before each test"""
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

        # Post.query.delete()
        # User.query.delete()

        db.drop_all()
        db.create_all()
        
        user = User(first_name="John", last_name="Doe", img_url="https://via.placeholder.com/150")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

        post = Post(title="My First Post!", content="Hello World!", user_id=self.user_id)

        db.session.add(post)
        db.session.commit()

    def tearDown(self):
        """clear anything remaining in the session"""

        db.session.rollback()


    def test_user_list(self):
        """tests if /user template is rendering correctly"""

        resp = self.client.get('/users')
        html = resp.get_data(as_text = True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Users</h1>', html)

    def test_show_form(self):
        """test if form to add new user renders correctly on page"""

        resp = self.client.get('/users/new')
        html = resp.get_data(as_text = True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Create a user</h1>', html)
        self.assertIn('<button>Add User</button>', html)

    def test_show_user(self):
        """tests if test user is being shown on the page"""

        resp = self.client.get(f'{self.user_id}')
        html = resp.get_data(as_text = True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h2>John Doe</h2>', html)

    def test_add_user(self):
        """tests if user is added in correctly using form"""

        user = {"first-name": "Mary", "last-name": "Jane", "img-url": "https://via.placeholder.com/150"}

        resp = self.client.post('/users/new', data = user, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Mary Jane', html)

    def test_edit_user(self):
        """tests if a user is edited correctly"""

        user = User.query.get_or_404(self.user_id)
        user.first_name = "Edit"
        user.last_name = "Test"
        user.img_url = "https://via.placeholder.com/150"

        edited_user = {"first-name": user.first_name, "last-name": user.last_name, "img-url": user.img_url}

        resp = self.client.post(f'/users/{self.user_id}/edit', data = edited_user, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Edit Test', html)

    # Part 2

    def test_show_post_form(self):
        """tests if form to submit new post is shown correctly"""

        resp = self.client.get(f'/users/{self.user_id}/posts/new')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>Add Post for John Doe</h1>', html)

    def test_add_post(self):
        """tests if post is submitted correctly"""

        new_post = {"title": "My second post!", "content": "Hello world again!", "user_id": self.user_id}

        resp = self.client.post(f'/users/{self.user_id}/posts/new', data = new_post, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<a href="/posts/2">My second post!</a>', html)

    def test_show_post(self):
        """tests if a post is displayed correctly"""

        resp = self.client.get('/posts/1')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>My First Post!</h1>', html)

    def test_edit_post(self):
        """tests if function edits a post correctly"""

        post = Post.query.get_or_404(1)
        post.title = "I like cats"
        post.content = "I like cats very much"

        edited_post = {"title": post.title, "content": post.content}

        resp = self.client.post('/posts/1/edit', data = edited_post, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('<h1>I like cats</h1>', html)

    def test_delete_post(self):
        """tests if function deletes post correctly"""

        resp = self.client.post('/posts/1/delete', follow_redirects=True)

        self.assertEqual(resp.status_code, 200)



    
    




