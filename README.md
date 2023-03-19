# Ultimate Playlist Formatter
I've rebuilt this app in so many  languages I decided to just make it an actual complete thing instead of a personal project.

UltimatePlaylistFormatter is a Windows command line application for creating and formatting playlists. It supports local mp3 playlists and downloading from youtube using `yt-dlp`.

### The program requires `ffmpeg` to be installed (make sure to install the full build that includes `ffprobe`).

# Usage
See the [Options](#Options) table to see all the flags

Format: `ultimateplaylistformatter.exe "My Songs" path/to/songs path/to/output`

For extra help, you may use the `ultimateplaylistformatter.exe --help` command

## Options
| Flag                         | Description                                                      | Default |
|------------------------------|------------------------------------------------------------------|---------|
| --art (-a) [ART]             | The path of the album cover to use                               | None    | 
| --youtube (-y)               | Download input from YouTube.                                     | False   |
| --remove (-r) [REMOVE,...]   | Remove string (supports regex)                                   | None    |
| --extension (-e) [EXTENSION] | Specifies the preferred output audio format (mp3, m4a supported) | mp3     |