import os, sys
from song_split import song_split
from save_input_to_folder import save_to_folder
from generate_beatmap import create_beatmaps_from_spleeter_folders

def main():
    song_split()
    