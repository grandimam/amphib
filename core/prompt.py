import os

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import Template

from typing import Dict

from core.providers.base import BaseLLMProvider


class PromptManager:

	def __init__(
			self,
			provider: BaseLLMProvider,
			*,
			template_dir: str
	):
		self._provider = provider
		self._template_dir = template_dir
		self.env = Environment(
			loader=FileSystemLoader(template_dir),
			trim_blocks=True,
			lstrip_blocks=True,
		)
		self._templates: Dict[str, Template] = {}
		self._load_templates()

	def _load_templates(self):
		for filename in os.listdir(self._template_dir):
			if not filename.endswith(".jinja"):
				continue
			name = filename.removesuffix(".jinja")
			self._templates[name] = self.env.get_template(filename)
