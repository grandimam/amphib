import typer
from rich import print

from core import Amphib

from core.parsers import PDFParser
from core.prompt import JinjaPromptProvider
from core.prompt import PromptTemplate
from core.providers.chat import OpenRouterProvider

from core.config import settings

app = typer.Typer()


@app.command()
def run(file_path: str):
	runner = Amphib(
		parser=PDFParser(),
		model_provider=OpenRouterProvider(settings.openrouter_api_key),
		prompt_provider=JinjaPromptProvider(),
	)
	response = runner.run(file_path=file_path, prompt_name=PromptTemplate.LAYOUT.value)
	print(response)
