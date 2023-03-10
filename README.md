# Streamlink Kick plugin

A Simple [Kick.com](https://kick.com) plugin for [Streamlink](https://github.com/streamlink/streamlink).

## Install
* pip install [cloudscraper](https://pypi.org/project/cloudscraper)
* Copy the [kick.py](kick.py) file into one of the the [sideload directories](https://streamlink.github.io/cli/plugin-sideloading.html)


## Usage
```
streamlink kick.com/trainwreckstv best
streamlink --player-passthrough hls kick.com/video/bc5ad9f9-1f6c-414d-8ff8-f540f3ddcdea best
streamlink --player-passthrough http kick.com/trainwreckstv?clip=8113 best
```
