# Streamlink Kick plugin

A Simple [Kick.com](https://kick.com) plugin for [Streamlink](https://github.com/streamlink/streamlink). This plugin uses an extra dependency [cloudscraper](https://github.com/VeNoMouS/cloudscraper) in order to access KICK's cloudflare protected public API, until KICK provides a propor one.

## Install
* pip install [cloudscraper](https://pypi.org/project/cloudscraper)
* Copy the [kick.py](kick.py) file into one of the the [sideload directories](https://streamlink.github.io/cli/plugin-sideloading.html)


## Usage
```
streamlink kick.com/trainwreckstv best
streamlink kick.com/video/bc5ad9f9-1f6c-414d-8ff8-f540f3ddcdea best
streamlink kick.com/trainwreckstv?clip=8113 best
```

---
**NOTE**

You can passthrough the stream feed to your player using the [```--player-passthrough TYPES```](https://streamlink.github.io/cli.html#cmdoption-player-passthrough) option

---

