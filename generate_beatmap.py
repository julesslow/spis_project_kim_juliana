import os
import librosa

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
    create_beatmaps_from_spleeter_folders(spleeter_outputs_path)

