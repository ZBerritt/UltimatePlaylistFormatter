# Ultimate Playlist Formatter
I've rebuilt this app in so many  languages I decided to just make it an actual complete thing instead of a personal project.

UltimatePlaylistFormatter is a Windows command line application for creating and formatting playlists. It supports local mp3 playlists and downloading from youtube using `yt-dlp`.

### The program requires `ffmpeg` to be installed (make sure to install the full build that includes `ffprobe`).

# Usage
See the [Options](#Options) table to see all the flags

Format: `ultimateplaylistformatter.exe -i path/to/songs -n "My Songs" output/path`

For extra help, you may use the `ultimateplaylistformatter.exe --help` command

## Options
| Flag                         | Description                                                      | Required | Default |
|------------------------------|------------------------------------------------------------------|----------|---------|
| --input (-i) [INPUT]         | The input folder/youtube url                                     | Yes      | N/A     |
| --name (-n) [NAME]           | The name of the album/artist                                     | Yes      | N/A     |
| --art (-a) [ART]             | The path to the art to use                                       | No       | N/A     | 
| --youtube (-y)               | Download input from YouTube.                                     | No       | False   |
| --remove (-r) [REMOVE,...]   | Remove string (supports regex)                                   | No       | N/A     |
| --extension (-e) [EXTENSION] | Specifies the preferred output audio format (mp3, m4a supported) | No       | mp3     |