# Ultimate Playlist Formatter
A Windows command line application for creating and formatting mp3/m4a playlists. 

### The program requires `ffmpeg` to be installed and be on the system PATH.

## About
This is a super beefed up version of an application I recreate whenever I'm learning a new programming language. Since I've rebuilt this app so times, I've decided to just make it an actual complete application.

It supports mp3 and m4a audio files and can even download from a YouTube playlist using the python package for `yt-dlp`.

## Usage
See the [Options](#Options) table to see all the flags

Format: `ultimateplaylistformatter.exe "My Songs" path/to/songs path/to/output [options...]`

For more help, you may use the `ultimateplaylistformatter.exe --help` command

## Options
| Flag                         | Description                                                          | Default       |
|------------------------------|----------------------------------------------------------------------|---------------|
| --cover (-c) [COVER]         | The path of the album cover to use                                   | None          |
| --artist (-a) [ARTIST]       | The artist of the album                                              | Same as album |
| --remove (-r) [REMOVE,...]   | Remove string (supports regex)                                       | None          |
| --extension (-e) [EXTENSION] | Specifies the preferred output audio format (mp3, m4a supported)     | mp3           |
| --no-format (-n)             | Skips formatting step (useful for just downloading YouTube playlists | False         |

## Building
I personally use `pyinstaller` for building to an executable. You can install it with `pip install pyinstaller`

Run the following command to build: `pyinstaller main.py -F -n "ultimateplaylistformatter"`