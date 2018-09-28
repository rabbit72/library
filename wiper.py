import click

import db


@click.command()
@click.option(
    "--all",
    "-a",
    "delete_data",
    is_flag=True,
    default=False,
    help="This flag for cleaning all database",
)
@click.option(
    "--number",
    "-n",
    "book_id",
    type=int,
    help="Book ID for deleting the book",
)
def enter_point(book_id, delete_data):
    if delete_data:
        deleted_data = db.delete_all_data()
        click.echo("Data base was cleaned")
        click.echo(f"{deleted_data['book']} books deleted")
        click.echo(f"{deleted_data['author']} authors deleted")
    else:
        is_correct = db.delete_book_by_id(book_id)
        if is_correct:
            click.echo("Book deleting was success")
        else:
            click.echo("Book was not found")


if __name__ == "__main__":
    enter_point()
