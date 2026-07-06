import os
import typer

from core.parsers import PDFParser
from core.prompt import PromptManager
from core.providers.chat import LLMProvider

from core.config import settings


app = typer.Typer()


@app.command()
def main(file_path: str):
	parser = PDFParser().parse(file_path)
	provider = LLMProvider(os.environ.get(settings.openrouter_key))
	prompt = PromptManager(provider, template_dir=settings.template_dir)
