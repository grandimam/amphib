import os
import typer

from core.parsers import PDFParser
from core.prompt import PromptHandler
from core.providers.chat import LLMProvider

from core.config import settings
from rich import print

app = typer.Typer()


@app.command()
def run(file_path: str):
	resume_text: str = PDFParser().parse(file_path)
	prompt_handler = PromptHandler(settings.prompt_dir)
	sys_msg = prompt_handler.get('layout')

	provider = LLMProvider(os.environ.get(settings.openrouter_api_key))
	response = provider.chat(
		model_name=settings.model_name,
		messages=[
			{"role": "system", "content": sys_msg},
			{"role": "user", "content": resume_text},
		],
		temperature=0.0,
		top_p=0.9
	)
	print(response)
