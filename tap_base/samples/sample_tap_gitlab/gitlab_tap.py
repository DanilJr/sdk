"""Sample tap test for tap-gitlab."""

from typing import List
from tap_base import Tap, Stream
from tap_base.samples.sample_tap_gitlab.gitlab_rest_streams import (
    ProjectsStream,
    ReleasesStream,
    IssuesStream,
    CommitsStream,
)
from tap_base.samples.sample_tap_gitlab.gitlab_graphql_streams import (
    GraphQLCurrentUserStream,
)
from tap_base.samples.sample_tap_gitlab.gitlab_globals import (
    PLUGIN_NAME,
    ACCEPTED_CONFIG_OPTIONS,
    REQUIRED_CONFIG_SETS,
)


STREAM_TYPES = [
    ProjectsStream,
    ReleasesStream,
    IssuesStream,
    CommitsStream,
    GraphQLCurrentUserStream,
]


class SampleTapGitlab(Tap):
    """Sample tap for Gitlab."""

    name: str = PLUGIN_NAME
    accepted_config_keys = ACCEPTED_CONFIG_OPTIONS
    required_config_options = REQUIRED_CONFIG_SETS

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [
            stream_class(config=self.config, state={}) for stream_class in STREAM_TYPES
        ]


# CLI Execution:

cli = SampleTapGitlab.cli
