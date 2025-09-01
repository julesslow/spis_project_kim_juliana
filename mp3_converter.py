# import yt_dlp, sys, os

# def convert_yt_to_mp3(url, cookies_path=None):
#     # This dictionary holds the options for yt-dlp
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '320',
#         }],
#         'outtmpl': os.path.join("input", '%(title)s.mp3'), # Output filename template
#     }
    
#     # Add the cookies option if a cookie file path is provided and it exists
#     if cookies_path and os.path.exists(cookies_path):
#         ydl_opts['cookiefile'] = cookies_path
    
#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])
#     print(f"Successfully converted {url} to MP3.")

# if __name__ == "__main__":
#     if len(sys.argv) > 1:
#         url_from_terminal = sys.argv[1]
        
#         # Define the path to your cookies file here
#         # Make sure to replace this with the correct path to your cookies.txt file
#         # Example: cookies_file = "/home/vscode/my_project/cookies.txt"
#         cookies_file = "www.youtube.com_cookies.txt"
        
#         # Check if the cookies file path is provided as a second command-line argument
#         if len(sys.argv) > 2:
#             cookies_file = sys.argv[2]
            
#         convert_yt_to_mp3(url_from_terminal, cookies_file)
#     else:
#         print("Please provide a YouTube URL as a command-line argument.")

import yt_dlp
import sys
import os

def convert_yt_to_mp3(url, cookies_path=None):
    """
    Converts a YouTube video to an MP3 file and returns the path to the new file.

    Args:
        url (str): The URL of the YouTube video.
        cookies_path (str, optional): The path to a cookies file for private videos.
                                     Defaults to None.

    Returns:
        str: The full file path of the newly created MP3 file, or None if an error occurs.
    """
    # Create the output folder if it doesn't exist
    output_folder = "input"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    # The dictionary holds the options for yt-dlp
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
    
    # Add the cookies option if a cookie file path is provided and it exists
    if cookies_path and os.path.exists(cookies_path):
        ydl_opts['cookiefile'] = cookies_path

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
    if len(sys.argv) > 1:
        url_from_terminal = sys.argv[1]
        
        # Define the path to your cookies file here
        cookies_file = "www.youtube.com_cookies.txt"
        
        # Check if the cookies file path is provided as a second command-line argument
        if len(sys.argv) > 2:
            cookies_file = sys.argv[2]
            
        # Call the function and get the returned path
        new_file_path = convert_yt_to_mp3(url_from_terminal, cookies_file)
        
        if new_file_path:
            print(f"The new MP3 file is located at: {new_file_path}")
        else:
            print("Failed to get the file path.")
    else:
        print("Please provide a YouTube URL as a command-line argument.")