import typer

from cli import analyze

app = typer.Typer()
app.add_typer(analyze.app, name='analyze')

if __name__ == "__main__":
	app()
