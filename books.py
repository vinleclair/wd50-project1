import csv

from project import db
from project.models import Book

def import_books():
    f = open("books.csv")
    reader = csv.reader(f)
    next(f)
    for isbn, title, author, year in reader:
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        print("Added book %s from %s published in %s with isbn: %s." % (title, author, year, isbn))
    db.session.commit()
    print("Book Import Successful")

