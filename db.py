import sqlalchemy
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker

import models

# dialect+driver://username:password@host:port/database
db = sqlalchemy.create_engine("postgresql://postgres:pass@localhost/")

Session = sessionmaker(db)
SESSION = Session()

try:
    models.base.metadata.create_all(db)
except OperationalError:
    exit("Check connection to DB")


def get_statistic():
    authors = SESSION.query(models.Author)
    books = SESSION.query(models.Book)
    return len(tuple(books)), len(tuple(authors))


def add_book(title: str, year: int = None, authors: set = frozenset(), update=False):
    book = get_book(title, year, authors)
    if book:
        return
    SESSION.add(models.Book(title, year))
    SESSION.commit()
    _id = get_book(title, year, set()).id
    __create_links_book_author(_id, __get_authors_id(authors, add_new_authors=True))


def add_author(name: str):
    SESSION.add(models.Author(name))
    SESSION.commit()


def get_author(name: str):
    try:
        author = SESSION.query(models.Author).filter_by(name=name)[0]
    except IndexError:
        author = None
    return author


def get_book(title: str, year: int, authors: set):
    books = list(SESSION.query(models.Book).filter_by(title=title, year=year))
    for book in books:
        if __get_book_author_names(book.id) == authors:
            return book
    return None


def delete_book_by_id(_id: int) -> bool:
    try:
        book = SESSION.query(models.Book).filter_by(id=_id).delete()
        SESSION.commit()
    except:
        SESSION.rollback()
        book = False
    return bool(book)


def delete_all_data():
    try:
        num_deleted_books = SESSION.query(models.Book).delete()
        num_deleted_authors = SESSION.query(models.Author).delete()
        SESSION.commit()
    except:
        SESSION.rollback()
        num_deleted_books, num_deleted_authors = 0, 0
    return {
        "book": num_deleted_books,
        "author": num_deleted_authors,
    }


def __get_book_author_names(_id: int) -> set:
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


def __create_links_book_author(book_id, authors_id: dict):
    for author_id in authors_id.values():
        if not authors_id:
            continue
        SESSION.add(models.BooksAuthors(book_id, author_id))
    SESSION.commit()


def __get_authors_id(author_names: set, add_new_authors=False) -> dict:
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
