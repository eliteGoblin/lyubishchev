import click


@click.command()
def hello() -> None:
    click.echo("Hello World!")


if __name__ == "__main__":
    # execute only if run as the entry point into the program
    hello()
