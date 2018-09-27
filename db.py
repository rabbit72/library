import sqlalchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.exc import OperationalError
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
        Integer, ForeignKey("author.id"), nullable=False, primary_key=True
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


def get_statistic():
    authors = SESSION.query(Author)
    books = SESSION.query(Book)
    return len(tuple(books)), len(tuple(authors))


def add_book(title: str, year: int = None, authors: set = None):
    book = get_book(title, year, authors)

    if book:  # and flag_update == True then update_book
        return

        # book_authors = get_book_author_names(book.id)
        # if book_authors == authors:
        #     print("100% the same book")
        #     return
        # else:
        #     print("Book exists but authors are different")
        #     return

    SESSION.add(Book(title, year))
    SESSION.commit()
    _id = get_book(title, year, set()).id
    create_links_book_author(_id, get_authors_id(authors, add_new_authors=True))


def add_author(name: str):
    SESSION.add(Author(name))
    SESSION.commit()


def get_author(name: str):
    try:
        author = SESSION.query(Author).filter_by(name=name)[0]
    except IndexError:
        author = None
    return author


def get_book_author_names(_id: int) -> set:
    request = SESSION.execute(
        """
        SELECT name FROM author
                   INNER JOIN books_authors ON books_authors.author_id = author.id
                   INNER JOIN book ON book.id = books_authors.book_id
            WHERE book.id = :id;""",
        {"id": _id},
    )
    authors_names = request.fetchall()
    authors_names = {name[0] for name in authors_names}
    if authors_names:
        return authors_names
    return set()


def get_book(title: str, year: int, authors: set):
    books = list(SESSION.query(Book).filter_by(title=title, year=year))
    for book in books:
        if get_book_author_names(book.id) == authors:
            return book
    return None


def create_links_book_author(book_id, authors_id: dict):
    for author_id in authors_id.values():
        if not authors_id:
            continue
        SESSION.add(BooksAuthors(book_id, author_id))
        SESSION.commit()


def get_authors_id(author_names: set, add_new_authors=False) -> dict:
    authors_id = dict()
    for name in author_names:
        author = get_author(name)
        if not author:
            if add_new_authors:
                add_author(name)
                author = get_author(name)
            else:
                author = None
        authors_id[name] = author.id
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
