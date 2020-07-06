# AllTwitchClips-dl
## Script to download all Twitch clips from a channel using youtube-dl.

Requires a file called creds.txt in the same directory with Twitch API credentials (see template-for-creds.txt)

Requires youtube-dl installed (https://github.com/ytdl-org/youtube-dl)

Config file legend:
* number-of-clips - number of clips to download per page (max 100, default 64)
* pagination - enable to get URLS on every available page (default 1 = on)
* broadcaster-id - Broadcaster ID to find clips for (ex. 12345678)
* error-logging - enable to create an error log file (default 0 = off)
* clip-logging - enable to keep a log of clips that have already been downloaded and not attempt to download them again (default 1 = on)
* download-path - path to save downloaded clips
* ytdl-flags - flags for youtube-dl, seperated by spaces (ex. -c -i)