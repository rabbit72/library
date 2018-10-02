from configparser import ConfigParser

import psycopg2
from psycopg2 import sql


def get_config():
    config = ConfigParser()
    config.read("../config.ini")
    if config.has_section("postgres"):
        return dict(config["postgres"])
    return {"user": "postgres", "password": "pass", "host": "localhost", "port": 5432}


conf = get_config()
CONN = psycopg2.connect(
    user=conf["user"], password=conf["password"], host=conf["host"], port=conf["port"]
)
CURSOR = CONN.cursor()


def __send_request(sql_request, variables=None):
    CURSOR.execute(sql.SQL(sql_request), variables)
    CONN.commit()


def __fetch_reply(sql_request, variables=None):
    CURSOR.execute(sql.SQL(sql_request), variables)
    return CURSOR.fetchall()


def add_author(name: str):
    sql_request = "INSERT INTO author(name) VALUES (%s);"
    __send_request(sql_request, (name,))
    return get_author(name, only_id=True)


def get_statistic():
    all_authors = __fetch_reply("SELECT count(*) FROM author;")[0][0]
    all_books = __fetch_reply("SELECT count(*) FROM book;")[0][0]
    return all_books, all_authors


def get_book_author_names(_id: int) -> set:
    sql_request = """
        SELECT name FROM author
            INNER JOIN books_authors ON books_authors.author_id = author.id
            INNER JOIN book ON book.id = books_authors.book_id
        WHERE book.id = %s;"""
    variables = (_id,)
    authors_names = __fetch_reply(sql_request, variables)
    authors_names = {name[0] for name in authors_names}
    if authors_names:
        return authors_names
    return set()


def get_book(title: str, year: int, authors: set, only_id=False):
    sql_request = """
        SELECT id, title, year, last_update FROM book
        WHERE title = %s and year = %s
        ORDER BY last_update DESC;"""

    if year is None:
        sql_request = """
                SELECT id, title, year, last_update FROM book
                WHERE title = %s and year is %s
                ORDER BY last_update DESC;"""
    books = __fetch_reply(sql_request, (title, year))
    for book in books:
        book_id = book[0]
        if get_book_author_names(book_id) == authors:
            if only_id:
                return book_id
            return book
    return None


def __create_links_book_author(book_id, authors_id: dict):
    for author_id in authors_id.values():
        if not authors_id:
            continue
        create_link = """
            INSERT INTO books_authors(book_id, author_id) VALUES (%s, %s)"""
        __send_request(create_link, (book_id, author_id))


def add_book(title: str, year: int = None, authors: set = frozenset(), update=False):
    book = get_book(title, year, authors)
    if book:
        return
    create_new_book = "INSERT INTO book(title, year) VALUES (%s, %s);"
    __send_request(create_new_book, (title, year))
    new_book_id = get_book(title, year, set(), only_id=True)

    __create_links_book_author(
        new_book_id, __get_authors_id(authors, add_new_authors=True)
    )


def get_author(name: str, only_id=False):
    sql_request = "SELECT id, name, last_update FROM author WHERE name = %s;"
    authors = __fetch_reply(sql_request, (name,))
    if authors:
        author = authors[0]
        if only_id:
            return author[0]
        return author
    return None


def delete_book_by_id(_id: int) -> bool:
    book_id = __fetch_reply("SELECT id FROM book WHERE id = %s", (_id,))
    if not book_id:
        return False
    __send_request("DELETE FROM book WHERE id = %s", (_id,))
    return True


def delete_all_data():
    books_before, authors_after = get_statistic()
    __send_request("DELETE FROM book;")
    __send_request("DELETE FROM author;")
    return {"book": books_before, "author": authors_after}


def create_index():
    create_index_author = """
    CREATE INDEX idx_author ON author
    USING zombodb ((author.*))
    WITH (url='elasticsearch:9200/');"""
    create_index_book = """
        CREATE INDEX idx_book ON book
        USING zombodb ((book.*))
        WITH (url='elasticsearch:9200/');"""
    __send_request(create_index_author)
    __send_request(create_index_book)


def __get_authors_id(author_names: set, add_new_authors=False) -> dict:
    authors_id = dict()
    for name in author_names:
        author_id = get_author(name, only_id=True)
        if not author_id and add_new_authors:
            author_id = add_author(name)
        authors_id[name] = author_id
    return authors_id


def search_book_by_name(name: str) -> list:
    pattern = f'name: "{name}"'
    sql_authors = "SELECT id FROM author WHERE author ==> %s;"
    authors = __fetch_reply(sql_authors, (pattern,))

    sql_books = """
        SELECT book.*
        FROM book
            INNER JOIN books_authors ON books_authors.book_id = book.id
            INNER JOIN author ON author.id = books_authors.author_id
        WHERE author.id = %s;"""

    books = []
    for author in authors:
        author_id = author[0]
        books_result = __fetch_reply(sql_books, (author_id,))
        books.extend(books_result)
    return books


def search_book_by_title(title: str) -> list:
    pattern = f'title: "{title}"'
    sql_request = "SELECT * FROM book WHERE book ==> %s;"
    books = __fetch_reply(sql_request, (pattern,))
    return books


def search_book_by_year(year) -> list:
    if year is None:
        sql_request = "SELECT * FROM book WHERE book.year is NULL;"
        return __fetch_reply(sql_request)
    elif isinstance(year, int):
        sql_request = "SELECT * FROM book WHERE book.year = %s;"
        return __fetch_reply(sql_request, (year,))
    else:
        return []
