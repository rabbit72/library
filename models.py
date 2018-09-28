from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base


base = declarative_base()


class Author(base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<Author({self.name})>"


class Book(base):
    __tablename__ = "book"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=True)

    def __init__(self, title, year=None):
        self.title = title
        self.year = year

    def __repr__(self):
        return f"<Book({self.title})>"


class BooksAuthors(base):
    __tablename__ = "books_authors"
    author_id = Column(
        Integer, ForeignKey("author.id"), nullable=False, primary_key=True
    )
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False, primary_key=True)

    def __init__(self, book_id, author_id):
        self.book_id = book_id
        self.author_id = author_id

    def __repr__(self):
        return f"<Book-Author({self.book_id} - {self.author_id})>"
