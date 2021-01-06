"""Sample tap stream test for tap-gitlab."""

from pathlib import Path
from tap_base.authenticators import SimpleAuthenticator
from typing import Any, Dict, List, Union

from tap_base.streams.rest import RESTStream, URLArgMap
from tap_base.helpers import listify

SCHEMAS_DIR = Path("./tap_base/samples/sample_tap_gitlab/schemas")


class GitlabStream(RESTStream):
    """Sample tap test for gitlab."""

    url_base = "https://gitlab.com/api/v4"

    @property
    def authenticator(self) -> SimpleAuthenticator:
        """Return an authenticator for REST API requests."""
        http_headers = {"Private-Token": self.config.get("auth_token")}
        if self.config.get("user_agent"):
            http_headers["User-Agent"] = self.config.get("user_agent")
        return SimpleAuthenticator(http_headers=http_headers)

    def get_query_params(self) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """Expose any needed config values into the URL parameterization process.

        If a list of dictionaries is returned, one call will be made for each item
        in the list. For GitLab, this is necessary when each call must reference a
        specific `project_id`.
        """
        if "{project_id}" not in self.url_suffix:
            return super().get_query_params()  # Default behavior
        return [
            {"project_id": project_id, "start_date": self.config.get("start_date")}
            for project_id in listify(self.config.get("project_ids"))
        ]


class ProjectsStream(GitlabStream):
    name = "projects"
    url_suffix = "/projects/{project_id}?statistics=1"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "projects.json"


class ReleasesStream(GitlabStream):
    name = "releases"
    url_suffix = "/projects/{project_id}/releases"
    primary_keys = ["project_id", "commit_id", "tag_name"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "releases.json"


class IssuesStream(GitlabStream):
    name = "issues"
    url_suffix = "/projects/{project_id}/issues?scope=all&updated_after={start_date}"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "issues.json"


class CommitsStream(GitlabStream):
    name = "commits"
    url_suffix = (
        "/projects/{project_id}/repository/commits?since={start_date}&with_stats=true"
    )
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "commits.json"
