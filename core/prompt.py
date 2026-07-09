import os
from enum import Enum
from typing import Dict
from typing import Protocol
from typing import TypeVar

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template

from core.config import settings

T = TypeVar("T")


class PromptTemplate(Enum):
	LAYOUT = 'layout'
	EVALUATE = 'evaluate'
	EXTRACT = 'extract'


class PromptProvider[T](Protocol):
	name: str

	def load_template(self): ...

	def get_template(self, prompt_section: str) -> str: ...


class JinjaPromptProvider(PromptProvider[str]):
	name: str = 'jinja'

	def __init__(self):
		self._prompt_dir = settings.prompt_dir
		self.env = Environment(
			loader=FileSystemLoader(self._prompt_dir),
			trim_blocks=True,
			lstrip_blocks=True,
		)
		self._templates: Dict[str, Template] = {}
		self.load_template()

	def load_template(self):
		for filename in os.listdir(self._prompt_dir):
			if not filename.endswith(".jinja"):
				continue
			name = filename.removesuffix(".jinja")
			self._templates[name] = self.env.get_template(filename)

	def get_template(self, prompt_section: str, **kwargs) -> str:
		if prompt_section not in self._templates:
			raise ValueError(f'{prompt_section} not found')
		template: Template = self._templates.get(prompt_section)
		return template.render(**kwargs)
