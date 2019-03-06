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


    # tests
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Book Reviews', response.data)
        self.assertIn(b'Search', response.data)
        self.assertIn(b'Books', response.data)
        self.assertIn(b'Book Reviews', response.data)
        self.assertIn(b'Goodreads', response.data)
        self.assertIn(b'Add Book', response.data)

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
