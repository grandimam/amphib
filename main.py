import typer

from cli.analyze import analyze
from cli.evaluate import evaluate
from cli.extract import extract

app = typer.Typer()
app.command()(analyze)
app.command()(evaluate)
app.command()(extract)

if __name__ == "__main__":
    app()
