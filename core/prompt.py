import os

from enum import Enum

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template

from typing import Dict


class PromptTemplate(Enum):
	LAYOUT = 'layout'


class PromptProvider:

	def __init__(self, prompt_dir: str):
		self._prompt_dir = prompt_dir
		self.env = Environment(
			loader=FileSystemLoader(self._prompt_dir),
			trim_blocks=True,
			lstrip_blocks=True,
		)
		self._templates: Dict[str, Template] = {}
		self._load()

	def _load(self):
		for filename in os.listdir(self._prompt_dir):
			if not filename.endswith(".jinja"):
				continue
			name = filename.removesuffix(".jinja")
			self._templates[name] = self.env.get_template(filename)

	def get(self, prompt_name):
		if prompt_name not in self._templates:
			raise ValueError(f'{prompt_name} not found')
		template: Template = self._templates.get(prompt_name)
		return template.render()
