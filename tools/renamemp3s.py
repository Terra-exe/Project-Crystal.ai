import os

# Directory containing the mp3 files
directory = "D:\\tmp\\glaum mp3s\\"

# List all files in the directory
files = os.listdir(directory)

# Loop through each file
for file in files:
    # Check if the file ends with ".mp3"
    if file.endswith(".mp3"):
        # Split the file name to remove "- {track_name.mp3}"
        new_name = file.split(" - {")[0] + ".mp3"
        # Construct full file paths
        old_file_path = os.path.join(directory, file)
        new_file_path = os.path.join(directory, new_name)
        # Rename the file
        os.rename(old_file_path, new_file_path)

# List the renamed files to confirm
renamed_files = os.listdir(directory)
print(renamed_files)
