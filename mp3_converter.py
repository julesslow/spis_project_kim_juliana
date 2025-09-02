import yt_dlp
import sys
import os

def convert_yt_to_mp3(url, username=None, password=None):
    """
    Converts a YouTube video to an MP3 file and returns the path to the new file.

    Args:
        url (str): The URL of the YouTube video.
        username (str, optional): The username for authentication.
        password (str, optional): The password for authentication.

    Returns:
        str: The full file path of the newly created MP3 file, or None if an error occurs.
    """
    # Create the output folder if it doesn't exist
    output_folder = "input"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    # This dictionary holds the options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        # Use os.path.join for cross-platform path creation.
        # '%(title)s.%(ext)s' ensures the final file extension is correct.
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
    }

    # Add username and password to the options if they are provided
    if username and password:
        ydl_opts['username'] = username
        ydl_opts['password'] = password
    
    # Initialize a variable to store the filename
    new_mp3_path = None
    
    # We use a custom hook to capture the filename after the download is complete.
    def my_hook(d):
        nonlocal new_mp3_path
        if d['status'] == 'finished':
            # The 'info_dict' contains the path to the downloaded file.
            new_mp3_path = d['info_dict']['_filename']

    ydl_opts['progress_hooks'] = [my_hook]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # This will trigger the progress hook when finished
            ydl.download([url])
            print(f"Successfully converted {url}.")
            return new_mp3_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) > 2:
        url_from_terminal = sys.argv[1]
        username = sys.argv[2]
        password = sys.argv[3]
            
        # Call the function with the URL, username, and password
        new_file_path = convert_yt_to_mp3(url_from_terminal, username, password)
        
        if new_file_path:
            print(f"The new MP3 file is located at: {new_file_path}")
        else:
            print("Failed to get the file path.")
    else:
        print("Please provide a YouTube URL, username, and password as command-line arguments.")