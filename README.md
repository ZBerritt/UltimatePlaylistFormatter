# Ultimate Playlist Formatter
I've rebuilt this app in so many  languages I decided to just make it an actual complete thing instead of a personal project.

UltimatePlaylistFormatter is a command line application for creating and formatting mp3 playlists. It supports local mp3 playlists and downloading from youtube using `yt-dlp`.

### The program requires `ffmpeg` to be installed (make sure to install the full build that includes `ffprobe`).

# Usage
See the [Options](#Options) table to see all the flags

Format: `ultimateplaylistformatter -i path/to/songs -n "My Songs" output/path`

For extra help, you may use the `ultimateplaylistformatter --help` command

## Options
| Flag                       | Description                    | Required |
|----------------------------|--------------------------------|----------|
| --input (-i) [INPUT]       | The input folder/youtube url   | Yes      |
| --name (-n) [NAME]         | The name of the album/artist   | Yes      |
| --art (-a) [ART]           | The path to the art to use     | No       |
| --youtube (-y)             | Download input from YouTube.   | No       |
| --remove (-r) [REMOVE,...] | Remove string (supports regex) | No       |
