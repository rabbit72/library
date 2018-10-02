import click

import db


def print_books(books: list, only_id=False, limit=None):
    if not books:
        click.echo("Books were not founded. Change your request and try again")
    if limit:
        books = books[:limit]
    for i, (_id, title, year, authors) in enumerate(books, start=1):
        if only_id:
            click.echo(f"{i}. {_id}")
        else:
            click.echo(f"{i}. Title: {title}")
            click.echo(f"   ID: {_id}")
            click.echo(f"   Year: {year}")
            click.echo(f"   Authors: {', '.join(authors)}")
            click.echo()


@click.command()
@click.option("--author", "-a", type=str, default=None, help="Name author")
@click.option("--name", "-n", type=str, default=None, help="Book title")
@click.option("--year", "-y", type=int, default=None, help="Year when book was written")
@click.option("--limit", "-l", type=int, default=None, help="Limit book for print")
@click.option("--simple", "-s", is_flag=True, default=False, help="return only ID")
def enter_point(author, name, year, limit, simple):
    if not any((author, name, year)):
        click.echo("Enter one of them or all [Author, Book name, Year]")
        exit()
    options = {
        db.search_book_by_year: year,
        db.search_book_by_title: name,
        db.search_book_by_name: author,
    }
    new_options = options.copy()
    for func, value in new_options.items():
        if value is None:
            del options[func]

    results = [set(func(value)) for func, value in options.items()]

    books = list(set.intersection(*results))
    books_with_authors = []
    for book_id, title, year, last_update in books:
        authors_names = list(db.get_book_author_names(book_id))
        books_with_authors.append((book_id, title, year, authors_names))
    print_books(books_with_authors, simple, limit)


if __name__ == "__main__":
    enter_point()
