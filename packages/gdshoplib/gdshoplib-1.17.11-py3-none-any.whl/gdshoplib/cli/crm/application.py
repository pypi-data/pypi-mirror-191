import typer

from gdshoplib.cli.crm.order import app as order

app = typer.Typer()

app.add_typer(order, name="order")


if __name__ == "__main__":
    app()
