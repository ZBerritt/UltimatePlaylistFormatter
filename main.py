import argparse
import os
import re
import subprocess
import sys
import tempfile
from yt_dlp import YoutubeDL
from shutil import which, rmtree

SUPPORTED_IMAGES = [
    "png",
    "jpg",
    "jpeg"
]

SUPPORTED_EXTENSIONS = [
    "mp3",
    "m4a"
]


# TODO: Possibly include the ffmpeg binary to prevent requirements
def main():
    # Check ffmpeg install
    if which("ffmpeg") is None:
        print("FFMPEG is not installed or is not on the PATH. (https://ffmpeg.org/download.html)")
        return

    # Get arguments
    parser = argparse.ArgumentParser(
        prog="UltimatePlaylistFormatter",
        description="Fully functional youtube/mp3 playlist formatter (requires ffmpeg)"
    )
    parser.add_argument("name", help="The name of the album")
    parser.add_argument("input", help="The input folder/youtube url")
    parser.add_argument("destination", help="Playlist destination folder")
    parser.add_argument("-c", "--cover", help="The path of the album cover to use")
    parser.add_argument("-r", "--remove", help="Remove string (supports regex)", nargs="*")
    parser.add_argument("-e", "--extension", help="Specifies the preferred output audio format (mp3, m4a supported)",
                        default="mp3", choices=SUPPORTED_EXTENSIONS)

    args = parser.parse_args()

    # Verify arguments
    if args.cover and (not os.path.isfile(args.cover) or os.path.splitext(args.cover.lower())[1][1:] not in SUPPORTED_IMAGES):
        print("Art file is not a valid image file (png or jpeg)")
        return

    if not os.path.isdir(args.destination):
        os.mkdir(args.destination)

    # Check if YouTube playlist
    youtube_input = re.match(r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/playlist\?list=(.*)$', args.input)

    extension = args.extension

    # Step 1 - Get songs
    if youtube_input:
        song_location = download_playlist(args.input, extension)
    else:
        song_location = args.input

    # Verify location
    if not os.path.isdir(song_location):
        print("An error has occurred when retrieving the songs. Please verify your input URL/location.")
        return clean_exit(None)
    songs = get_songs(song_location)

    if len(songs) == 0:
        print("No songs were found!")
        clean_exit(song_location)

    # Step 2 - Parse song names'
    parsed_names = [os.path.splitext(song)[0] for song in songs]
    for reg in args.remove:
        parsed_names = [re.sub(rf"{reg}", "", song).strip() for song in parsed_names]

    # Step 3 - FFMPEG to destination
    for song, name in zip(songs, parsed_names):
        source_file = os.path.join(song_location, song)
        title = args.name
        out_file_name = f"{name} - {title} OST.{extension}"
        destination_file = os.path.join(args.destination, out_file_name)

        # Start FFMPEG
        command = ["ffmpeg", "-y"]
        if args.cover is not None:
            command += ["-i", args.cover]
        command += ["-i", source_file]
        command += ["-map", "0:0"]
        if args.cover is not None:
            command += ["-map", "1:0"]
        command += ["-codec", "copy"]
        command += ["-metadata", f"title={name}"]
        command += ["-metadata", f"album={title}"]
        command += ["-metadata", f"artist={title}"]
        command.append(destination_file)
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)  # Do not print to console
        print("Wrote:", out_file_name)

    # Exit
    subprocess.Popen(rf'explorer "{args.destination}"')  # Open folder when done
    clean_exit(song_location)


def get_songs(location: str) -> list:
    songs = []
    for root, dirs, files in os.walk(location):
        for filename in files:
            if os.path.splitext(filename)[1][1:] in SUPPORTED_EXTENSIONS:
                songs.append(filename)
    return songs


def download_playlist(playlist: str, extension: str) -> str:
    print("Downloading playlist:", playlist)
    temp_folder = tempfile.mkdtemp(prefix="upf-")
    output_template = os.path.join(temp_folder, "%(title)s.%(ext)s")
    ydl_opts = {
        'format': 'bestaudio',  # Format here shouldn't matter since we'll be using ffmpeg to convert
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': extension,
        }],
        'outtmpl': output_template,
        'logger': CleanLogger()
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(playlist)

    print("YouTube Download complete")
    return temp_folder


def clean_exit(temp_folder: str):
    if temp_folder is not None:
        rmtree(temp_folder)
    sys.exit(0)


# Represents a clean logger to make the command line not overloaded
class CleanLogger:
    def debug(self, msg):
        if msg.startswith("[download] Downloading item"):
            print(msg)

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print("ERROR: An error has occurred processing the provided YouTube playlist. Please make sure the URL is "
              "valid.", file=sys.stderr)
        print(msg, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
