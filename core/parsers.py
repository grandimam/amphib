from typing import Protocol

import pymupdf
from pymupdf4llm import to_markdown


class BaseParser[T](Protocol):

	def parse(self, file_path: str) -> T: ...


class PDFParser(BaseParser[str]):

	def parse(self, file_path: str) -> str:
		with pymupdf.open(file_path) as doc:
			pages = range(doc.page_count)
			return to_markdown(doc, pages=pages)
