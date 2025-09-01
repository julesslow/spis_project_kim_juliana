from song_split import song_split
from mp3_converter import convert_yt_to_mp3
from generate_beatmap import create_beatmaps_from_spleeter_folders

def main():
    song = input("Enter a youtube url")
    convert_yt_to_mp3(song)
    song_split()
    