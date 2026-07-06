from pydantic import BaseModel


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
