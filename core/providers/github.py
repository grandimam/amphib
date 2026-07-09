import os
from typing import runtime_checkable

import requests

from core.providers.base import BaseClientProvider
from core.schemas import GitHubProfile, GithubProjectInfo


@runtime_checkable
class GithubProvider(BaseClientProvider[GitHubProfile]):
	BASE_URL: str = 'https://api.github.com/users/'
	OPENSOURCE: str = "open_source"
	SELF_PROJECT: str = "self_project"

	def __init__(self, api_token: str, username: str):
		self._api_token = api_token
		self._username = username

	def headers(self):
		return {
			"Authorization": f"token {self._api_token}"
		}

	def fetch(self) -> GitHubProfile:
		request_url = os.path.join(self.BASE_URL, self._username)
		response = requests.get(request_url, headers=self.headers())
		if response.status_code == 200:
			return GitHubProfile.model_validate_json(response.json())

	@staticmethod
	def fetch_contributions_count(owner: str, contributors_data):
		user_contributions = 0
		total_contributions = 0

		for contributor in contributors_data:
			if isinstance(contributor, dict):
				contributions = contributor.get("contributions", 0)
				total_contributions += contributions

				if contributor.get("login", "").lower() == owner.lower():
					user_contributions = contributions

		return user_contributions, total_contributions

	def fetch_repo_contributors(self, owner: str, repo_name: str) -> list[dict]:
		request_url = f"https://api.github.com/repos/{owner}/{repo_name}/contributors"
		status_code, contributors_data = requests.get(request_url, headers=self.headers())
		return contributors_data if status_code == 200 else None

	def get_repos(self):
		request_url: str = os.path.join(self.BASE_URL, self._username, "/repos")
		params = {"sort": "updated", "per_page": 100, "type": "all"}
		status, data = requests.get(request_url, headers=self.headers(), params=params)

		projects = []
		for repo in data:
			# This is a rule, that is not projected into the prompt, but hardcoded here!
			if repo.get("fork") and repo.get("forks_count", 0) < 5:
				continue
			repo_name = repo.get("name")
			contrib_data = self.fetch_repo_contributors(self._username, repo_name)
			contributor_count = len(contrib_data)
			user_contrib, total_contrib = self.fetch_contributions_count(self._username, contrib_data)
			project_type = self.OPENSOURCE if contributor_count > 1 else self.SELF_PROJECT
			project_info = GithubProjectInfo.model_validate(
				{
					**repo,
					"project_type": project_type,
					"author_commit_count": user_contrib,
					"total_commit_count": total_contrib,
				}
			)
			projects.append(project_info)
		projects.sort(key=lambda x: x["github_details"]["stars"], reverse=True)
		return projects

	def get_projects(self):
		pass
