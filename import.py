import csv

from project import db
from project.models import Book

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    next(f)
    db.create_all()
    for isbn, title, author, year in reader:
        book = Book(isbn=isbn, title=title, author=author, year=year)
        db.session.add(book)
        print("Added book %s from %s published in %s with isbn: %s." % (title, author, year, isbn))
    db.session.commit()
    print("--Import Successful--")

if __name__ == "__main__":
    main()
