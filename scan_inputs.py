import os
import json
import hashlib
from datetime import datetime

# --- Configuration ---
JSON_OUTPUT_FILE = "file_data.json"
FOLDER_TO_SCAN = "/workspaces/spis_project_kim_juliana/input"
OUTPUT_FOLDER_BASE = "/workspaces/spis_project_kim_juliana/outputs" 

def calculate_hash(file_path):
    """Calculates the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except IOError:
        print(f"Could not read file: {file_path}")
        return None

def scan_folder(folder_path):
    """Scans a folder and returns a list of dictionaries with file metadata."""
    all_files_data = []
    print(f"Scanning folder: {folder_path}...")

    for root, _, files in os.walk(folder_path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            try:
                file_info = {
                    "file_name": filename,
                    "file_path": file_path,
                    "file_size_bytes": os.path.getsize(file_path),
                    "file_type": os.path.splitext(filename)[1].lower(),
                    "date_modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
                    "sha256_hash": calculate_hash(file_path)
                }

                # --- START: NEW LOGIC TO FIND OUTPUT FOLDER ---
                # Check if the scanned file is an mp3.
                if file_info["file_type"] == ".mp3":
                    # Get the filename without the extension (e.g., "song" from "song.mp3").
                    base_name = os.path.splitext(filename)[0]
                    # Construct the full path where the output folder should be.
                    expected_output_path = os.path.join(OUTPUT_FOLDER_BASE, base_name)
                    
                    # Check if that directory actually exists.
                    if os.path.isdir(expected_output_path):
                        file_info["output_folder_path"] = expected_output_path

                        # --- START: New logic to find .wav files ---
                        wav_files_found = []
                        # List all items inside the found output folder.
                        for item in os.listdir(expected_output_path):
                            # Check if the item ends with .wav (case-insensitive).
                            if item.lower().endswith('.wav'):
                                wav_path = os.path.join(expected_output_path, item)
                                if os.path.isfile(wav_path):
                                    wav_files_found.append(wav_path)
                        
                        # Add the list of found .wav files to our record.
                        file_info["output_wav_files"] = wav_files_found
                        # --- END: New logic ---

                    else:
                        file_info["output_folder_path"] = "Not found"
                        file_info["output_wav_files"] = [] 
                else:
                    # For non-mp3 files, just set the field to None.
                    file_info["output_folder_path"] = None
                    file_info["output_wav_files"] = []
                # --- END: NEW LOGIC ---

                if file_info["sha256_hash"]:
                    all_files_data.append(file_info)
                    
            except FileNotFoundError:
                print(f"File not found during scan: {file_path}")
                continue
    
    return all_files_data


if __name__ == "__main__":
    if not os.path.exists(FOLDER_TO_SCAN):
        os.makedirs(FOLDER_TO_SCAN)
        print(f"Created directory '{FOLDER_TO_SCAN}'. Please add files and run again.")
    else:
        # 1. Scan the folder and get all the file data.
        scanned_data = scan_folder(FOLDER_TO_SCAN)
        
        # 2. Write the collected data to the JSON file.
        with open(JSON_OUTPUT_FILE, 'w') as f:
            # json.dump writes the Python list to the file as JSON.
            # indent=4 makes it nicely formatted and easy to read.
            json.dump(scanned_data, f, indent=4)
        
        print(f"\n✅ Scan complete. Data for {len(scanned_data)} files saved to '{JSON_OUTPUT_FILE}'.")