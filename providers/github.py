import os
import requests

from schemas import GitHubProfile
from typing import runtime_checkable
from providers.base import BaseClientProvider


@runtime_checkable
class GithubProvider(BaseClientProvider[GitHubProfile]):
	BASE_URL: str = 'https://api.github.com/users/'

	def __init__(self, api_token: str, username: str):
		self._api_token = api_token
		self._username = username

	def fetch(self) -> GitHubProfile:
		request_url = os.path.join(self.BASE_URL, self._username)
		response = requests.get(request_url)
		if response.status_code == 200:
			return GitHubProfile.model_validate_json(response.json())
