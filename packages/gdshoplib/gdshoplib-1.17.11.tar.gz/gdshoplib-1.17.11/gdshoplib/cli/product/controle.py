import typer

from gdshoplib.apps.product import Product

app = typer.Typer()


@app.command()
def sku_set():
    for page in Product.query(
        params={
            "filter": {
                "and": [
                    {"property": "Наш SKU", "rich_text": {"is_empty": True}},
                    {"property": "Цена (eur)", "number": {"is_not_empty": True}},
                ]
            }
        },
    ):
        sku = page.generate_sku()
        while not Product.query(filter={"sku": sku}):
            sku = page.generate_sku()

        page.notion.update_prop(
            page.id, params={"properties": {"Наш SKU": [{"text": {"content": sku}}]}}
        )
        print(Product(page.id).sku)
