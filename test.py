from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserTests(TestCase):

    def setUp(self):
        """things to run before each test"""
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

        User.query.delete()
        user = User(first_name="John", last_name="Doe", img_url="https://via.placeholder.com/150")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

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
        html = resp.get_data(as_text = True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Mary Jane', html)

