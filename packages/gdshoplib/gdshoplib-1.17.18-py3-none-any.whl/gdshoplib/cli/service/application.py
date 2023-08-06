import typer

from gdshoplib.cli.service.vk import app as vk

app = typer.Typer()

app.add_typer(vk, name="vk")

if __name__ == "__main__":
    app()
