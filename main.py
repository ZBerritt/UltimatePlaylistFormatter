import argparse
import os
import re
import subprocess
import sys
import tempfile
from yt_dlp import YoutubeDL
from shutil import which, rmtree

SUPPORTED_EXTENSION = [
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
    parser.add_argument("-i", "--input", required=True, help="The input folder/youtube url")
    parser.add_argument("-n", "--name", required=True, help="The name of the album")
    parser.add_argument("-a", "--art", help="The path to the art to use")
    parser.add_argument("-y", "--youtube", action="store_true",
                        help="Download input from YouTube.")
    parser.add_argument("-r", "--remove", help="Remove string (supports regex)", nargs="*")
    parser.add_argument("-e", "--extension", help="Specifies the preferred output audio format (mp3, m4a supported)",
                        default="mp3", choices=SUPPORTED_EXTENSION)
    parser.add_argument("destination", help="Playlist destination folder")

    args = parser.parse_args()

    # Verify arguments
    if args.art and (not os.path.isfile(args.art) or not args.art.lower().endswith(
            ('.png', '.jpg', '.jpeg'))):
        print("Art file is not a valid image file")
        return

    if not os.path.isdir(args.destination):
        os.mkdir(args.destination)

    extension = args.extension

    # Step 1 - Get songs
    if args.youtube:
        song_location = download_playlist(args.input, extension)
    else:
        song_location = args.input

    # Verify location
    if not os.path.isdir(song_location):
        print("An error has occurred when downloading songs." if args.youtube else "Song directory could not be"
                                                                                   "found.")
        return clean_exit(song_location)
    songs = get_songs(song_location)

    # Step 2 - Parse song names
    parsed_names = []
    for song in songs:
        # Remove extension
        name = os.path.splitext(song)[0]
        for reg in args.remove:
            name = re.sub(rf"{reg}", "", name)
            name = name.strip()  # Sorta fixes broken regex
        parsed_names.append(name)

    # Step 3 - FFMPEG to destination
    for i in range(len(songs)):
        song_file = os.path.join(song_location, songs[i])
        name = parsed_names[i]
        title = args.name
        out_file_name = f"{name} - {title} OST." + extension
        destination_file = os.path.join(args.destination, out_file_name)

        # Start FFMPEG
        command = ["ffmpeg", "-y"]
        if args.art is not None:
            command += ["-i", args.art]
        command += ["-i", song_file]
        command += ["-map", "0:0"]
        if args.art is not None:
            command += ["-map", "1:0"]
        command += ["-codec", "copy"]
        command += ["-metadata", f"title={name}"]
        command += ["-metadata", f"album={title}"]
        command += ["-metadata", f"artist={title}"]
        command.append(destination_file)
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("Wrote:", out_file_name)

    # Exit
    subprocess.Popen(rf'explorer "{args.destination}"')
    clean_exit(song_location)


def get_songs(location: str) -> list:
    songs = []
    for root, dirs, files in os.walk(location):
        for filename in files:
            if os.path.splitext(filename)[1][1:] in SUPPORTED_EXTENSION:
                songs.append(filename)
    return songs


def download_playlist(playlist: str, extension: str) -> str:
    print("Downloading playlist:", playlist)
    temp_folder = tempfile.mkdtemp(prefix="upf-")
    output_template = os.path.join(temp_folder, "%(title)s.%(ext)s")
    ydl_opts = {
        'format': 'mp3/bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': extension,
        }],
        'outtmpl': output_template,
        'logger': CleanLogger()
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download(playlist)

    print("Download complete")
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
        print(msg)


if __name__ == "__main__":
    main()
