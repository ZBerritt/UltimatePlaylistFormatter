import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from shutil import which


SUPPORTED_IMAGES = {"png", "jpg", "jpeg"}
SUPPORTED_EXTENSIONS = {"mp3", "m4a"}


def main():
    check_requirements()
    args = parse_arguments()
    verify_arguments(args)

    print_info("📥 Checking audio files...")
    song_location = args.input

    check_song_location(song_location)
    songs = get_songs(song_location)

    if not songs:
        print_warning("⚠ No songs were found in the input folder.")
        sys.exit(1)

    print_info("🎼 Parsing song metadata...")
    parsed_names = [Path(song).stem for song in songs]
    for pattern in args.remove:
        parsed_names = [re.sub(pattern, "", name).strip() for name in parsed_names]

    print_info("🎧 Starting FFMPEG processing...")
    for song_file, name in zip(songs, parsed_names):
        source_path = Path(song_location) / song_file
        album = args.album
        artist = args.artist
        ext = args.extension
        output_name = f"{name} - {album}.{ext}" if album == artist else f"{name} - {artist} ({album}).{ext}"
        destination_path = Path(args.destination) / output_name

        ffmpeg_cmd = build_ffmpeg_command(source_path, destination_path, args.cover, name, album, artist, args.extension)
        subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print_success(f"✔ Wrote: {output_name}")

    print_info("📂 Opening destination folder...")
    open_folder(args.destination)


def check_requirements():
    if which("ffmpeg") is None:
        print_error("FFMPEG is not installed or not in your system PATH. Install it from https://ffmpeg.org/download.html")
        sys.exit(1)


def parse_arguments():
    def valid_regex(value):
        try:
            return re.compile(value)
        except re.error as e:
            raise argparse.ArgumentTypeError(f"Invalid regex pattern '{value}': {e}")
        
    parser = argparse.ArgumentParser(
        prog="UltimatePlaylistFormatter",
        description="📀 Format a local audio playlist into a properly tagged album."
    )
    parser.add_argument("album", help="Album name")
    parser.add_argument("input", help="Local folder path containing audio files")
    parser.add_argument("destination", help="Output folder path for formatted audio")
    parser.add_argument("-c", "--cover", help="Path to album cover (PNG/JPG)")
    parser.add_argument("-a", "--artist", help="Artist name (defaults to album name if omitted)")
    parser.add_argument("-r", "--remove", nargs="+", type=valid_regex, help="Regex patterns to remove from filenames")
    parser.add_argument("-e", "--extension", default="mp3", choices=SUPPORTED_EXTENSIONS, help="Output format (default: mp3)")

    return parser.parse_args()


def verify_arguments(args):
    if args.cover:
        cover_path = Path(args.cover)
        if not cover_path.is_file() or cover_path.suffix[1:].lower() not in SUPPORTED_IMAGES:
            print_error("Cover art must be a valid PNG or JPEG image.")
            sys.exit(1)

    args.artist = args.artist or args.album
    Path(args.destination).mkdir(parents=True, exist_ok=True)


def check_song_location(song_location):
    if not Path(song_location).is_dir():
        print_error("Invalid song location. Please provide a valid folder path.")
        sys.exit(1)


def get_songs(location: str) -> list[str]:
    location = Path(location)
    return [f.name for f in location.glob("*") if f.suffix[1:] in SUPPORTED_EXTENSIONS]


def build_ffmpeg_command(source_file, dest_file, cover_path, title, album, artist, extension):
    command = ["ffmpeg", "-y", "-i", source_file]
    
    if cover_path:
        command += ["-i", cover_path]
        
        if extension.lower() == "m4a":
            # M4A format - embed cover as attachment
            command += [
                "-map", "0:a",           # Map audio from first input
                "-map", "1:v",           # Map image from second input
                "-c:a", "copy",          # Copy audio codec
                "-c:v", "copy",          # Copy image as-is
                "-disposition:v:0", "attached_pic"  # Mark image as attached picture
            ]
        elif extension.lower() == "mp3":
            # MP3 format - embed cover as album art
            command += [
                "-map", "0:a",           # Map audio from first input
                "-map", "1:v",           # Map image from second input
                "-c:a", "copy",          # Copy audio codec
                "-c:v", "copy",          # Copy image as-is
                "-id3v2_version", "3",   # Use ID3v2.3 for better compatibility
                "-metadata:s:v", "title=Album cover",
                "-metadata:s:v", "comment=Cover (front)"
            ]
    else:
        # No cover art - just copy audio
        command += ["-map", "0:a", "-c:a", "copy"]
    
    # Add metadata tags (escape special characters if needed)
    metadata_tags = [
        ("title", title),
        ("album", album),
        ("artist", artist)
    ]
    
    for tag, value in metadata_tags:
        if value:  # Only add non-empty metadata
            # Escape quotes and special characters in metadata values
            escaped_value = value.replace('"', '\\"')
            command += ["-metadata", f"{tag}={escaped_value}"]
    
    # Add output file
    command.append(dest_file)
    
    return command


def open_folder(path: str | Path):
    subprocess.Popen(rf'explorer "{Path(path)}"' if os.name == 'nt' else ["xdg-open", str(path)])


# ✨ Terminal Output Helpers
def print_success(msg): print(f"\033[92m{msg}\033[0m")
def print_error(msg): print(f"\033[91m{msg}\033[0m", file=sys.stderr)
def print_warning(msg): print(f"\033[93m{msg}\033[0m")
def print_info(msg): print(f"\033[94m{msg}\033[0m")


if __name__ == "__main__":
    main()