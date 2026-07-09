from datetime import datetime

from pydantic import BaseModel, Field


class GitHubProfile(BaseModel):
	username: str
	name: str | None = None
	bio: str | None = None
	location: str | None = None
	company: str | None = None
	public_repos: int | None = None
	followers: int | None = None
	following: int | None = None
	created_at: str | None = None
	updated_at: str | None = None
	avatar_url: str | None = None
	blog: str | None = None
	twitter_username: str | None = None
	hireable: bool = False


class GithubProjectDetails(BaseModel):
	stars: int
	forks: int
	languages: list[str] | None = Field(default_factory=list)
	description: str | None = None
	created_at: datetime | None = None
	updated_at: datetime | None = None
	topics: str | None = None
	open_issues: int | None = None
	size: str | None = None
	fork: bool = False
	archived: bool = False


class GithubProjectInfo(BaseModel):
	name: str
	github_url: str
	live_url: str | None = None
	description: str | None = None
	technologies: list[str] = Field(default_factory=list)
	project_type: str | None = None
	contributor_count: int | None = None
	author_commit_count: int | None = None
	total_commit_count: int | None = None
	github_details: GithubProjectDetails
