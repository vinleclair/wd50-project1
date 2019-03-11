from books import import_books
from project import db
from project.models import Book, User, Review
from datetime import datetime


# drop all of the existing database tables
db.drop_all()

# create the database and the database table
db.create_all()

# insert book data
import_books()

# insert user data
admin_user = User(email='vinleclair@gmail.com', plaintext_password='limeman', role='admin')
user1 = User('hibou@yahoo.com', 'password1234')
user2 = User('spameggsham@gmail.com', 'PaSsWoRd')
user3 = User('blaa@blaa.com', 'MyFavPassword')
db.session.add(admin_user)
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# insert review data
review1 = Review(2, 4, 4, 'good book')
db.session.add(review1)

# commit the changes
db.session.commit()
