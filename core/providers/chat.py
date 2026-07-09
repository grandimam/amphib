from typing import Union
from typing import Protocol
from core.types import MESSAGE

import litellm


class ModelProvider[T](Protocol):
	type: str

	def chat(
			self,
			model_name: str,
			messages: MESSAGE,
			*,
			temperature: Union[float | None] = None,
			top_p: Union[float | None] = None,
	) -> T: ...


class OpenRouterProvider(ModelProvider[str]):
	type: str = 'openrouter'

	def __init__(self, api_key: str):
		self._api_key = api_key

	def chat(
			self,
			model_name: str,
			messages: MESSAGE,
			*,
			temperature: Union[float | None] = None,
			top_p: Union[float | None] = None,
	) -> str:
		response = litellm.completion(
			model=model_name,
			messages=messages,
			temperature=temperature,
			top_p=top_p,
			api_key=self._api_key,
		)
		return response.choices[0].message.content
