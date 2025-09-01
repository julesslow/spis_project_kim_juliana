from pytube import YouTube
from pydub import AudioSegment
import os

def convert_yt_to_mp3_pytube(url):
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    downloaded_file = audio_stream.download()

    base, ext = os.path.splitext(downloaded_file)
    new_mp3_file = base + '.mp3'

    # Convert to MP3 using pydub
    audio = AudioSegment.from_file(downloaded_file)
    audio.export(new_mp3_file, format="mp3")

    # Optional: Remove the original downloaded audio file
    os.remove(downloaded_file)
    print(f"Successfully converted {url} to MP3.")

if __name__ == "__main__":
    
    convert_yt_to_mp3_pytube()
