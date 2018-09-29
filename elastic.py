from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient


host = "localhost"
port = 9200

ES = Elasticsearch(([{"host": host, "port": port}]))
INDICES = IndicesClient(ES)
if not INDICES.exists(index="books"):
    ES.indices.create(index='books', ignore=400)
if not INDICES.exists(index="authors"):
    ES.indices.create(index='authors', ignore=400)


def add_author(_id: int, name: str):
    ES.index(
        index="authors",
        doc_type="author",
        body={"name": name, "id": _id}
    )


def search_author(name: str, only_id=False, only_first=False) -> list:
    res = ES.search(index="authors", body={"query": {"match": {"name": name}}})
    authors = [author["_source"] for author in res['hits']['hits']]
    if authors:
        if only_first:
            authors = [authors[0]]
        if only_id:
            return [author["id"] for author in authors]
    return authors


def delete_all_authors():
    ES.delete_by_query(index="authors", body={"query": {"match_all": {}}})


def add_book(_id: int, title: str, year: int):
    ES.index(
        index="books",
        doc_type="book",
        body={"title": title, "id": _id, "year": year}
    )


def search_book(title: str, only_id=False, only_first=False) -> list:
    res = ES.search(index="books", body={"query": {"match": {"title": title}}})
    books = [book["_source"] for book in res['hits']['hits']]
    if books:
        if only_first:
            books = [books[0]]
        if only_id:
            return [book["id"] for book in books]
    return books


def delete_book_by_id(_id: int):
    ES.delete_by_query(index="books", body={"query": {"match": {"id": _id}}})


def delete_all_books():
    ES.delete_by_query(index="books", body={"query": {"match_all": {}}})
