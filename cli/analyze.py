import os
import typer

from core.parsers import PDFParser
from core.providers.chat import ModelProvider
from core.prompt import PromptProvider
from core.prompt import PromptTemplate

from core.config import settings

from core import Amphib

from rich import print

app = typer.Typer()


@app.command()
def run(file_path: str):
	runner = Amphib(
		parser=PDFParser(),
		model_provider=ModelProvider(os.environ.get(settings.openrouter_api_key)),
		prompt_provider=PromptProvider(settings.prompt_dir),
	)
	response = runner.run(file_path=file_path,  prompt_name=PromptTemplate.LAYOUT.value)
	print(response)

