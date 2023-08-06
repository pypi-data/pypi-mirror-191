import typer

from gdshoplib.apps.finance.storage import Storage
from gdshoplib.apps.product import Product

app = typer.Typer()


@app.command()
def amount(base_price="now"):
    print(f"{base_price}: {Storage().amount(Product.query(), base_price=base_price)}")
