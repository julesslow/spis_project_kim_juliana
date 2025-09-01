import yt_dlp, sys, os

def convert_yt_to_mp3(url, cookies_path=None):
    # This dictionary holds the options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': os.path.join("input", '%(title)s.mp3'), # Output filename template
    }
    
    # Add the cookies option if a cookie file path is provided and it exists
    if cookies_path and os.path.exists(cookies_path):
        ydl_opts['cookiefile'] = cookies_path
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"Successfully converted {url} to MP3.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url_from_terminal = sys.argv[1]
        
        # Define the path to your cookies file here
        # Make sure to replace this with the correct path to your cookies.txt file
        # Example: cookies_file = "/home/vscode/my_project/cookies.txt"
        cookies_file = "www.youtube.com_cookies.txt"
        
        # Check if the cookies file path is provided as a second command-line argument
        if len(sys.argv) > 2:
            cookies_file = sys.argv[2]
            
        convert_yt_to_mp3(url_from_terminal, cookies_file)
    else:
        print("Please provide a YouTube URL as a command-line argument.")