# Streamlink Kick plugin

A Simple [Kick.com](https://kick.com) plugin for [Streamlink](https://github.com/streamlink/streamlink). This plugin uses an extra dependency [cloudscraper](https://github.com/VeNoMouS/cloudscraper) in order to try to access KICK's cloudflare protected public API, until KICK provides a more streamlined way to do so.

## Install
* pip install [cloudscraper](https://pypi.org/project/cloudscraper)
  * For Windows users with streamlink builds which come bundled with an embedded Python environment, regular pip will not suffice and a ModuleNotFoundError will be raised when running streamlink. You can fix this by adding ```--target=<StreamLinkInstallPath>\pkgs```
* Copy the [kick.py](kick.py) file into one of the the [sideload directories](https://streamlink.github.io/cli/plugin-sideloading.html)


## Usage
```
streamlink kick.com/trainwreckstv best
streamlink kick.com/video/c32a463d-4f4e-44f8-a5f3-88e8c5c8e720 best
streamlink kick.com/trainwreckstv?clip=clip_01H6V5QHN7VMYHKNYVY7B6FRWW best
```

---
**TIP**

You can passthrough the stream feed to your player using the [```--player-passthrough TYPES```](https://streamlink.github.io/cli.html#cmdoption-player-passthrough) option

---

