"""Sample tap test for tap-google-analytics."""

import json
from pathlib import Path
from typing import List

from tap_base.tap_base import Tap
from tap_base.samples.sample_tap_google_analytics.ga_tap_stream import (
    GASimpleSampleStream,
    SampleGoogleAnalyticsStream,
)
from tap_base.samples.sample_tap_google_analytics.ga_globals import (
    PLUGIN_NAME,
    ACCEPTED_CONFIG_OPTIONS,
    REQUIRED_CONFIG_SETS,
)

REPORT_DEFS_FILE = "tap_base/samples/sample_tap_google_analytics/resources/default_report_definitions.json"
REPORT_DEFS = json.loads(Path(REPORT_DEFS_FILE).read_text())


class SampleTapGoogleAnalytics(Tap):
    """Sample tap for GoogleAnalytics."""

    name: str = PLUGIN_NAME
    accepted_config_keys = ACCEPTED_CONFIG_OPTIONS
    required_config_options = REQUIRED_CONFIG_SETS
    default_stream_class = SampleGoogleAnalyticsStream

    def discover_streams(self) -> List[SampleGoogleAnalyticsStream]:
        """Return a list of all streams."""
        return [GASimpleSampleStream(config=self.config, state=self._state)]


cli = SampleTapGoogleAnalytics.cli
