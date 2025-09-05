# import sys
# import os
# import subprocess
# import shlex

# def song_split(song):
#     """
#     Splits a song into different audio components using Spleeter via a Docker container.

#     Args:
#         song (str): The full path to the input audio file on the host machine.
#     """
#     # Get just the filename from the full path.
#     filename = os.path.basename(song)

#     # Use a direct path for the model directory, as defined in devcontainer.json
#     model_directory = "/workspaces/ominous-space-journey-7v475wgpwrxj3pxgg/models" 

#     # Construct the Docker command as a list of arguments. This is the safest way
#     # to run external commands, as it avoids shell-specific syntax errors.
#     # We've removed shlex.quote from the final argument to fix the double-quoting issue.
#     command = [
#         "docker", "run", "--rm",
#         "-v", f"{os.path.abspath('input')}:/input",
#         "-v", f"{os.path.abspath('outputs')}:/output",
#         "-v", f"{model_directory}:/model",
#         "-e", "MODEL_PATH=/model",
#         "deezer/spleeter:3.8-4stems",
#         "separate", "-o", "/output", "-p", "spleeter:4stems", f"/input/{filename}"
#     ]

#     try:
#         # Run the command. `check=True` will raise an exception if the command fails.
#         # `capture_output=True` captures the standard output and error.
#         result = subprocess.run(command, check=True, capture_output=True, text=True)
#         print("Spleeter Output:", result.stdout)
#         print("Spleeter Error:", result.stderr)
#     except subprocess.CalledProcessError as e:
#         print(f"Error running Spleeter: {e}")
#         print("Spleeter Output:", e.stdout)
#         print("Spleeter Error:", e.stderr)
#         raise

# def main():
#     if len(sys.argv) > 1:
#         filename = sys.argv[1]
#         song_split(filename)
#     else:
#         print("Please provide a song filename as a command-line argument.")

# if __name__ == "__main__":
#     main()

import sys
import os
from spleeter.separator import Separator

def song_split(song):
    """
    Splits a song into different audio components using the native Spleeter library.
    
    Args:
        song (str): The full path to the input audio file.
    """
    
    # Check if the input file exists
    if not os.path.exists(song):
        print(f"Error: The file '{song}' does not exist.")
        return

    # Create the output directory if it doesn't exist
    output_directory = "outputs"
    os.makedirs(output_directory, exist_ok=True)
    
    print("Starting song split with Spleeter...")

    # Initialize the separator. This loads the pre-trained models.
    # We specify the 4-stems separation model.
    try:
        separator = Separator('spleeter:4stems')
    except Exception as e:
        print(f"Error initializing Spleeter: {e}")
        return

    # Perform the separation and save the output to the specified directory.
    try:
        # Spleeter needs a list of files to process
        separator.separate_to_file(song, output_directory)
        print("Song split completed successfully!")
    except Exception as e:
        print(f"Error during song separation: {e}")

def main():
    if len(sys.argv) > 1:
        # Get the filename from the command-line arguments
        filename = sys.argv[1]
        
        # Define the full path to the input song
        input_path = os.path.join("input", filename)
        
        song_split(input_path)
    else:
        print("Please provide a song filename as a command-line argument.")

if __name__ == "__main__":
    main()