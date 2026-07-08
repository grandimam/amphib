from core.parsers import BaseParser
from core.template import PromptProvider

from core.providers.chat import ModelProvider
from core.constants import SYSTEM
from core.constants import USER
from core.constants import CONTENT
from core.constants import ROLE

from core.config import settings


class Amphib:

	TOP_P: float = 0.9
	TEMPERATURE: float = 0.0

	def __init__(
			self,
			parser: BaseParser,
			model_provider: ModelProvider,
			prompt_provider: PromptProvider
	):
		self._parser = parser
		self._model_provider = model_provider
		self._prompt_provider = prompt_provider

	def run(
			self,
			file_path: str,
			prompt_name: str,
			model_name: str | None = settings.model_name,
	):
		parsed_resume: str = self._parser.parse(file_path)
		if not parsed_resume:
			raise Exception('Empty resume')

		sys_prompt: str = self._prompt_provider.get(prompt_name)

		return self._model_provider.chat(
			model_name=model_name,
			messages=[
				{
					ROLE: SYSTEM,
					CONTENT: sys_prompt
				},
				{
					ROLE: USER,
					CONTENT: parsed_resume
				},
			],
			temperature=self.TEMPERATURE,
			top_p=self.TOP_P
		)
