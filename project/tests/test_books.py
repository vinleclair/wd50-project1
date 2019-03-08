import os
import unittest

from project import app, db


TEST_DB = 'test.db'


class ProjectTests(unittest.TestCase):

    # setup and teardown

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app = app.test_client()
        db.create_all()

        self.assertEquals(app.debug, False)

    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

	# helper functions
    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
        )

    def register_user(self):
        self.app.get('/register', follow_redirects=True)
        self.register('patkennedy79@gmail.com', 'FlaskIsAwesome', 'FlaskIsAwesome')

    def login_user(self):
        self.app.get('/login', follow_redirects=True)
        self.login('patkennedy79@gmail.com', 'FlaskIsAwesome')

    def logout_user(self):
        self.app.get('/logout', follow_redirects=True)

    # test
    def test_main_page(self):
        self.register_user()
        self.logout_user()
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Book Reviews App', response.data)
        self.assertIn(b'Books', response.data)
        self.assertIn(b'Register', response.data)
        self.assertIn(b'Log In', response.data)

    def test_add_book_page(self):
        self.register_user()
        response = self.app.get('/add', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a New Book', response.data)

    def test_main_page_query_results(self):
        response = self.app.get('/add', follow_redirects=True)
        self.assertIn(b'Add a New Book', response.data)

    def test_add_book(self):
        response = self.app.post(
            '/add',
            data=dict(isbn='9780441172719',
                      title='Dune',
                      author='Frank Hebert',
                      year='1965'),
            follow_redirects=True)
        self.assertIn(b'New book, Dune, added!', response.data)

    def test_add_invalid_book(self):
        response = self.app.post(
            '/add',
            data=dict(isbn='',
                      title='Dune',
                      author='Frank Hebert',
                      year='1965'),
            follow_redirects=True)
        self.assertIn(b'ERROR! Book was not added.', response.data)
        self.assertIn(b'This field is required.', response.data)

if __name__ == "__main__":
    unittest.main()
