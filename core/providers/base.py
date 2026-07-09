from typing import Protocol, Union


class BaseLLMProvider(Protocol):

	def chat(
			self,
			model_name: str,
			messages: list,
			*,
			temperature: Union[float | None] = None,
			top_p: Union[float | None] = None,
	) -> str: ...


class BaseClientProvider[T](Protocol):

	def fetch(self) -> T: ...
