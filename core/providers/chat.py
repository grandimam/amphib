import litellm

from typing import Union


class LLMProvider:

	def __init__(self, api_key: str):
		self._api_key = api_key

	def chat(
			self,
			model_name: str,
			messages: list,
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
