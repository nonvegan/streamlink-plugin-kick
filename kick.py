"""
$description Kick
$url kick.com
$type live, vod
"""

import re
import cloudscraper

from streamlink.plugin import Plugin, pluginargument, pluginmatcher
from streamlink.plugin.api import validate
from streamlink.stream import HLSStream, HTTPStream
from streamlink.utils.parse import parse_json
from streamlink.exceptions import NoStreamsError, PluginError


@pluginmatcher(
    re.compile(
        # https://github.com/yt-dlp/yt-dlp/blob/9b7a48abd1b187eae1e3f6c9839c47d43ccec00b/yt_dlp/extractor/kick.py#LL33-L33C111
        r"https?://(?:www\.)?kick\.com/(?!(?:video|categories|search|auth)(?:[/?#]|$))(?P<channel>[\w_]+)$",
    ),
    name="live",
)
@pluginmatcher(
    re.compile(
        # https://github.com/yt-dlp/yt-dlp/blob/2d5cae9636714ff922d28c548c349d5f2b48f317/yt_dlp/extractor/kick.py#LL84C18-L84C104
        r"https?://(?:www\.)?kick\.com/video/(?P<video_id>[\da-f]{8}-(?:[\da-f]{4}-){3}[\da-f]{12})",
    ),
    name="vod",
)
@pluginmatcher(
    re.compile(
        r"https?://(?:www\.)?kick\.com/(?!(?:video|categories|search|auth)(?:[/?#]|$))(?P<channel>[\w_]+)\?clip=(?P<clip_id>[\d_]+)$",
    ),
    name="clip",
)
class KICK(Plugin):
    def _get_streams(self):
        API_BASE_URL = "https://kick.com/api"

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

        _CLIP_SCHEMA = validate.Schema(
            validate.parse_json(),
            {
                "clip": {"video_url": validate.url(path=validate.endswith(".mp4"))},
            },
            validate.get(("clip", "video_url")),
        )

        live, vod, clip = (
            self.matches["live"],
            self.matches["vod"],
            self.matches["clip"],
        )

        try:
            res = cloudscraper.create_scraper().get(
                "{0}/{1}/{2}".format(
                    API_BASE_URL,
                    *(
                        ["v1/channels", self.match["channel"]]
                        if live
                        else (
                            ["v1/video", self.match["video_id"]]
                            if vod
                            else ["v2/clips", self.match["clip_id"]]
                        )
                    )
                )
            )

            url = (
                _LIVE_SCHEMA if live else (_VIDEO_SCHEMA if vod else _CLIP_SCHEMA)
            ).validate(res.text)

        except (PluginError, TypeError) as err:
            return

        if clip:
            yield "source", HTTPStream(self.session, url)
        else:
            yield from HLSStream.parse_variant_playlist(self.session, url).items()


__plugin__ = KICK
