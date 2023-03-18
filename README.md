# Ultimate Playlist Formatter
A command line application for downloading & formatting mp3 playlists.

# Usage
See the [Options](#Options) table to see all the flags

Format: ultimateplaylistformatter -i path/to/songs -n "My Songs" output/path

For extra help, you may use the `ultimateplaylistformatter --help` command

## Options
| Flag                       | Description                    | Required |
|----------------------------|--------------------------------|----------|
| --input (-i) [INPUT]       | The input folder/youtube url   | Yes      |
| --name (-n) [NAME]         | The name of the album/artist   | Yes      |
| --art (-a) [ART]           | The path to the art to use     | No       |
| --youtube (-y)             | Download input from YouTube.   | No       |
| --remove (-r) [REMOVE,...] | Remove string (supports regex) | No       |
