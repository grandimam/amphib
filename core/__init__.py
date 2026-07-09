from core.config import settings
from core.constants import CONTENT
from core.constants import ROLE
from core.constants import SYSTEM
from core.constants import USER
from core.parsers import BaseParser
from core.providers.chat import ModelProvider
from core.prompt import JinjaPromptProvider


class Amphib:

	TOP_P: float = 0.9
	TEMPERATURE: float = 0.0

	def __init__(
			self,
			parser: BaseParser,
			model_provider: ModelProvider,
			prompt_provider: JinjaPromptProvider
	):
		self._parser = parser
		self._model_provider = model_provider
		self._prompt_provider = prompt_provider

	def run(
			self,
			file_path: str,
			prompt_name: str,
	):
		resume_content: str = self._parser.parse(file_path)
		system_prompt: str = self._prompt_provider.get_template(prompt_name)

		return self._model_provider.chat(
			model_name=settings.model_name,
			messages=[
				{
					ROLE: SYSTEM,
					CONTENT: system_prompt
				},
				{
					ROLE: USER,
					CONTENT: resume_content
				},
			],
			temperature=self.TEMPERATURE,
			top_p=self.TOP_P
		)
