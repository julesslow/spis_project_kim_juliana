import os, json
import librosa

def convert_to_json(input_folder="beatmaps", output_folder="beatmaps_json"):
    """
    Converts all text files in a specified folder to JSON files.

    Args:
        input_folder (str): The folder containing the .txt files.
        output_folder (str): The folder where the .json files will be saved.
    """
    # Create the output folder if it doesn't exist.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    # Check if the input folder exists.
    if not os.path.exists(input_folder):
        print(f"Error: The input folder '{input_folder}' was not found. Please ensure your beatmap .txt files are in this folder.")
        return

    # Loop through all files in the input folder.
    print(f"Looking for .txt files in '{input_folder}'...")
    found_files = False
    for filename in os.listdir(input_folder):
        # We only want to process .txt files.
        if filename.endswith(".txt"):
            found_files = True
            filepath_in = os.path.join(input_folder, filename)
            
            # This is the filename for the new JSON file.
            json_filename = filename.replace(".txt", ".json")
            filepath_out = os.path.join(output_folder, json_filename)
            
            print(f"Processing '{filename}'...")

            # Create a dictionary to hold our structured data.
            # This is the "JSON" part of the data before we save it.
            beatmap_data = {"notes": []}

            try:
                # Open and read the text file.
                with open(filepath_in, 'r') as f_in:
                    lines = f_in.readlines()
                    for line in lines:
                        # --- DEBUGGING ADDITION ---
                        print(f"  Reading line: '{line.strip()}'")
                        # --- END OF ADDITION ---
                        
                        # We assume each line is "x,y" and split it.
                        parts = line.strip().split(',')
                        
                        # --- DEBUGGING ADDITION ---
                        print(f"  Split parts: {parts}")
                        # --- END OF ADDITION ---
                        
                        # --- FIX: New logic to handle single-value lines ---
                        # We now expect a single value per line, which will be our timestamp.
                        try:
                            # Convert the single value to a float.
                            timestamp = float(line.strip())
                            
                            # We need to add notes in the correct format for the game.
                            # For now, we'll set a placeholder x-coordinate and use the timestamp as the y.
                            beatmap_data["notes"].append({"x": 400, "y": timestamp})

                        except ValueError:
                            # This will catch errors if the line is not a number.
                            print(f"Warning: Skipped line '{line.strip()}' because it was not a valid number.")
                        # --- END OF FIX ---
                
                # Write the new data to a .json file.
                with open(filepath_out, 'w') as f_out:
                    json.dump(beatmap_data, f_out, indent=4)
                    print(f"Successfully converted {filename} to {filepath_out}")

            except Exception as e:
                print(f"Error converting {filename}: {e}")
    
    if not found_files:
        print(f"No .txt files found in '{input_folder}'.")

def create_beatmaps_from_spleeter_folders(outputs_root):
    """
    Loops through Spleeter output subfolders to create beatmaps from all .wav files.
    """
    #print(f"Starting search in directory: {outputs_root}")
    found_files = False
    
    # os.walk will traverse the directory and all subdirectories
    for subdir, dirs, files in os.walk(outputs_root):
        #print(f"Checking directory: {subdir}")
        
        # Check if the directory has any files that end with .wav
        wav_files = [f for f in files if f.endswith('.wav')]
        if wav_files:
            #print(f"Found .wav files: {wav_files}")
            found_files = True
        
        for file in wav_files:
            file_path = os.path.join(subdir, file)
            #print(f"Attempting to process file: {file_path}")
            
            try:
                # Load the audio file
                x, sr = librosa.load(file_path)
                
                # Detect onsets
                onset_frames = librosa.onset.onset_detect(y=x, sr=sr)
                onset_times = librosa.frames_to_time(onset_frames)
                
                # Create and write to the beatmap file

                base_filename = os.path.splitext(os.path.basename(file_path))
                dir_name = os.path.basename(subdir)
                output_name = os.path.join("beatmaps", f"{dir_name}.{base_filename}.beatmap.txt")

                    
                    # Write the onset times to the beatmap file
                with open(output_name, 'wt') as f:
                    f.write('\n'.join(['%.4f' % onset_time for onset_time in onset_times]))
                    
                print(f"Beatmap created for {file_path} and saved to {output_name}")
            except Exception as e:
                print(f"ERROR: Could not process {file_path}. Reason: {e}")



# Example usage:
if __name__ == "__main__":
    spleeter_outputs_path = "outputs"
    absolute_outputs_path = os.path.abspath(spleeter_outputs_path)
    
    #print(f"Your script is looking for files in the following path: {absolute_outputs_path}")
    #print(f"Does this folder exist? {os.path.isdir(absolute_outputs_path)}")
    
    # Now you can use the absolute path to ensure the code works as expected
    #create_beatmaps_from_spleeter_folders(spleeter_outputs_path)
    convert_to_json()
