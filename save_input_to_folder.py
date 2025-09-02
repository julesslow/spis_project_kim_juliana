import os
import sys
import shutil

def save_to_folder(source_path, folder_name="input"):
    """
    Copies a file from a source path to a specified folder.

    Args:
        source_path (str): The full path of the file to be copied.
        folder_name (str): The name of the folder where the file will be saved.
    """
    # Check if the source file exists.
    if not os.path.exists(source_path):
        print(f"Error: The source file '{source_path}' was not found.")
        return

    # Create the folder if it doesn't already exist.
    try:
        os.makedirs(folder_name, exist_ok=True)
    except OSError as e:
        print(f"Error creating directory {folder_name}: {e}")
        return

    # Create the full file path for the destination.
    # We use the original filename to save it.
    file_name = os.path.basename(source_path)
    destination_path = os.path.join(folder_name, file_name)

    # Copy the file using shutil.
    try:
        shutil.copy(source_path, destination_path)
        print(f"Successfully saved '{file_name}' to '{destination_path}'")
    except shutil.Error as e:
        print(f"Error copying file: {e}")
    except IOError as e:
        print(f"Error writing to file {destination_path}: {e}")

if __name__ == "__main__":
    # Check if a file path was provided as a command-line argument.
    if len(sys.argv) > 1:
        file_to_save = sys.argv[1]
        save_to_folder(file_to_save)
    else:
        print("Please provide the path to a music file as a command-line argument.")
        print("Example: python3 save_input_to_folder.py 'path/to/your/song.mp3'")