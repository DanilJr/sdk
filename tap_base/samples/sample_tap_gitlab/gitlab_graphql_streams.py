"""Sample tap stream test for tap-gitlab.

# See the interactive GraphQL query builder for GitLab data models here:
#  - https://gitlab.com/-/graphql-explorer
"""

from datetime import datetime
from jinja2 import Template
from pathlib import Path
from typing import Dict, Union

from tap_base.authenticators import SimpleAuthenticator
from tap_base.streams import GraphQLStream

from tap_base.samples.sample_tap_google_analytics.ga_globals import PLUGIN_NAME


SITE_URL = "https://gitlab.com/graphql"

URLArgMap = Dict[str, Union[str, bool, int, datetime]]

SCHEMAS_DIR = Path("./tap_base/samples/sample_tap_gitlab/schemas")


class GitlabGraphQLStream(GraphQLStream):
    """Sample tap test for gitlab."""

    url_base = SITE_URL

    @property
    def authenticator(self) -> SimpleAuthenticator:
        """Return an authenticator for GraphQL API requests."""
        return SimpleAuthenticator(
            http_headers={"Authorization": f"token {self.config.get('auth_token')}"}
        )


class GraphQLCurrentUserStream(GitlabGraphQLStream):

    name = "currentuser"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "currentuser.json"
    query = """
        currentUser {
            name
        }
        """


class GraphQLProjectsStream(GitlabGraphQLStream):

    name = "projects"
    primary_keys = ["id"]
    replication_key = None
    schema_filepath = SCHEMAS_DIR / "projects-graphql.json"
    query = Template(
        """
        project(fullPath: "{{ project }}") {
            name
        }
        """
    ).render()
