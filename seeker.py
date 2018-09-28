import click

import db


@click.command()
@click.option("--author", "-a", type=str, help="Name author")
@click.option("--name", "-n", type=str, help="Book title")
@click.option("--year", "-y", type=int, help="Year when book was written")
@click.option("--simple", "-s", is_flag=True, default=False, help="Year when book was written")
def enter_point(author, name, year, simple):
    pass


if __name__ == "__main__":
    enter_point()
