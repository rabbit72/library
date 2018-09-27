import sqlalchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# dialect+driver://username:password@host:port/database
db = sqlalchemy.create_engine("postgresql://postgres:pass@localhost/")

base = declarative_base()


class Author(base):
    __tablename__ = "author"
    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    name = Column(String, unique=True, nullable=False)

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
        Integer, ForeignKey("author.id"), nullable=True, primary_key=True
    )
    book_id = Column(Integer, ForeignKey("book.id"), nullable=False, primary_key=True)

    def __init__(self, book_id, author_id):
        self.book_id = book_id
        self.author_id = author_id

    def __repr__(self):
        return f"<Book-Author({self.book_id} - {self.author_id})>"


Session = sessionmaker(db)
SESSION = Session()

try:
    base.metadata.create_all(db)
except OperationalError:
    exit("Check connection to DB")


def add_book(title: str, year=None, authors=None):
    SESSION.add(Book(title, year))
    SESSION.commit()
    _create_links_book_author(get_book_id(title), _get_authors_id(authors))


def add_author(name: str):
    SESSION.add(Author(name))
    SESSION.commit()


def get_author(name: str):
    try:
        author = SESSION.query(Author).filter_by(name=name)[0]
    except IndexError:
        author = []
    return author


def get_book_id(title: str):
    return SESSION.query(Book).filter_by(title=title)[0].id


def get_book_info(title: str):
    return SESSION.query(Book).filter_by(title=title)[0]


def _create_links_book_author(book_id, authors_id: list):
    if not authors_id:
        SESSION.add(BooksAuthors(book_id, None))

    for author_id in authors_id:
        SESSION.add(BooksAuthors(book_id, author_id))
    SESSION.commit()


def _get_authors_id(author_names: list) -> list:
    authors_id = []
    for name in author_names:
        author = get_author(name)
        if not author:
            add_author(name)
            author = get_author(name)
        authors_id.append(author.id)
    return authors_id


# # Create
# doctor_strange = Film(title="Doctor Strange", director="Scott Derrickson", year="2016")
# session.add(doctor_strange)
# session.commit()
#
# # Read
# films = session.query(Film)
# for film in films:
#     print(film.title)
#
# # Update
# doctor_strange.title = "Some2016Film"
# session.commit()
#
# # Delete
# session.delete(doctor_strange)
# session.commit()
