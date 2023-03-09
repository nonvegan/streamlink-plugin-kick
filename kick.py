"""
$description Kick
$url kick.com
$type live, vod
"""

import logging
import re
import cloudscraper

from streamlink.plugin import Plugin, pluginargument, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream.hls import HLSStream
from streamlink.utils.parse import parse_json
from streamlink.exceptions import NoStreamsError, PluginError

log = logging.getLogger(__name__)


@pluginmatcher(
    re.compile(
        # https://github.com/yt-dlp/yt-dlp/blob/9b7a48abd1b187eae1e3f6c9839c47d43ccec00b/yt_dlp/extractor/kick.py#LL33-L33C111
        r"https?://(?:www\.)?kick\.com/(?!(?:video|categories|search|auth)(?:[/?#]|$))(?P<channel>[\w_]+)",
    ),
    name="live",
)
@pluginmatcher(
    re.compile(
        # https://github.com/yt-dlp/yt-dlp/blob/2d5cae9636714ff922d28c548c349d5f2b48f317/yt_dlp/extractor/kick.py#LL84C18-L84C104
        r"https?://(?:www\.)?kick\.com/video/(?P<video>[\da-f]{8}-(?:[\da-f]{4}-){3}[\da-f]{12})",
    ),
    name="vod",
)
class KICK(Plugin):
    def _get_streams(self):
        self.low_latency = self.session.get_plugin_option("kick", "low-latency")

        API_BASE_URL = "https://kick.com/api/v1"

        _LIVE_SCHEMA = validate.Schema(
            validate.parse_json(),
            {
                "playback_url": validate.url(path=validate.endswith(".m3u8")),
                "livestream": {"is_live": True},
            },
            validate.get("playback_url"),
        )

        _VIDEO_SCHEMA = validate.Schema(
            validate.parse_json(),
            {
                "source": validate.url(path=validate.endswith(".m3u8")),
            },
            validate.get("source"),
        )

        try:
            res = cloudscraper.create_scraper().get(
                "{0}/{1}/{2}".format(
                    API_BASE_URL,
                    *(
                        ["channels", self.match["channel"]]
                        if self.matches["live"]
                        else ["video", self.match["video"]]
                    )
                )
            )

            hls_url = (
                _LIVE_SCHEMA if self.matches["live"] else _VIDEO_SCHEMA
            ).validate(res.text)

        except (PluginError, TypeError):
            return

        return HLSStream.parse_variant_playlist(self.session, hls_url)


__plugin__ = KICK
