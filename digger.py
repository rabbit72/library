import os
import zipfile
from io import BytesIO

import click
from lxml import etree

import db


def is_correct_ext(path: str) -> bool:
    formats = (".fb2", ".fb2.gz", ".fb2.zip")
    for ext in formats:
        if path.endswith(ext):
            return True
    return False


def get_tree_from_fb2(path):
    """
    :param path: path to file (fb2, fb2.gz, fb2.zip)
    :return: lxml.etree.ElementTree()
    """

    object_xml = path
    if path.endswith(".fb2.zip"):
        with zipfile.ZipFile(path) as _zip:
            file_name = _zip.namelist()
            if len(file_name) == 1:
                object_xml = BytesIO(_zip.read(file_name[0]))
            else:
                print("Many or none files in zip archive")
    tree = etree.parse(object_xml)  # TODO try to use xml SAX
    return tree


def fb2_path_generator(path_to_dir: str) -> str:
    for _root, _dir, file_names in os.walk(path_to_dir):
        for file_name in file_names:
            if is_correct_ext(file_name):
                yield os.path.abspath(os.path.join(_root, file_name))


def get_book_title(tag_element, namespace: str) -> str:
    tag = "book-title"
    book_title = [title for title in tag_element.iter(f"{namespace}{tag}")]
    if len(book_title) == 1:
        try:
            title = book_title[0].text.strip()
        except (TypeError, AttributeError):
            title = None
            print("Title didn't find")
        return title


def get_book_authors(tag_element, namespace: str) -> set:
    tag = "author"
    authors = set()

    all_authors_tag = list(tag_element.iter(f"{namespace}{tag}"))
    if not all_authors_tag:
        return authors

    for author in all_authors_tag:
        full_name = {"first-name": None, "middle-name": None, "last-name": None}
        for tag_object in author.getchildren():
            for tag_name in full_name:
                text = tag_object.text
                if text and tag_object.tag == f"{namespace}{tag_name}":
                    full_name[tag_name] = text.strip()

        try:
            name_in_tag = author.text.strip()
        except AttributeError:
            name_in_tag = None

        name_parts = [part for part in full_name.values() if part is not None]
        if not name_parts:
            if name_in_tag:
                str_name = name_in_tag
            else:
                continue
        else:
            str_name = " ".join(name_parts).title()
        authors.add(str_name)
    return authors


def get_created_year(tag_element, namespace: str) -> int:
    tag = "date"
    year = [year for year in tag_element.iter(f"{namespace}{tag}")]
    if len(year) == 1:
        try:
            created_year = int(year[0].text.strip())
        except (ValueError, AttributeError):
            created_year = None
        return created_year


def get_book_info(tree) -> dict:
    tag = "title-info"
    fb2_namespace = "{http://www.gribuser.ru/xml/fictionbook/2.0}"
    title_info = [title for title in tree.iter(f"{fb2_namespace}{tag}")][0]
    book_title = get_book_title(title_info, fb2_namespace)
    authors = get_book_authors(title_info, fb2_namespace)
    year = get_created_year(title_info, fb2_namespace)
    return {"book_title": book_title, "authors": authors, "year": year}


@click.command()
@click.option("--update", "-u", type=bool, default=False)
@click.argument("path", default="./books/", type=str)
def enter_point(path, update):
    path = "/home/dany/test_books/"
    if os.path.isdir(path):
        for path in fb2_path_generator(path):
            tree = get_tree_from_fb2(path)
            info = get_book_info(tree)
            db.add_book(info["book_title"], info["year"], info["authors"])
    elif os.path.isfile(path):
        info = get_book_info(get_tree_from_fb2(path))
        db.add_book(info["book_title"], info["year"], info["authors"])

    quantity_books, quantity_authors = db.get_statistic()
    print(
        f"{quantity_books} books and"
        f"{quantity_authors} authors have added in database"
    )


if __name__ == "__main__":
    enter_point()
