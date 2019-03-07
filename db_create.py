from books import import_books
from project import db
from project.models import Book, User


# drop all of the existing database tables
db.drop_all()

# create the database and the database table
db.create_all()

# insert book data
import_books()

# insert user data
user1 = User('hibou@yahoo.com', 'password1234')
user2 = User('spameggsham@gmail.com', 'PaSsWoRd')
user3 = User('blaa@blaa.com', 'MyFavPassword')
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# commit the changes for the recipes
db.session.commit()
