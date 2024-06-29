import os
import re

# Specify the directory containing the files
directory = r'D:\tmp\glaum mp3s\extra glaum mantras'  # Raw string to handle backslashes

# Regular expression pattern to match the undesired parts of the filename and forbidden characters
pattern = re.compile(r'_\d+(_\d+)*')
forbidden_chars = re.compile(r'[<>:"/\\|?*\']')

# Iterate over the files in the directory
for filename in os.listdir(directory):
    # Skip directories, only process files
    if os.path.isdir(os.path.join(directory, filename)):
        continue

    # Match and replace the undesired parts
    new_filename = re.sub(pattern, '', filename)
    new_filename = re.sub(forbidden_chars, '', new_filename)
    
    # Full paths for the old and new filenames
    old_file = os.path.join(directory, filename)
    new_file = os.path.join(directory, new_filename)

    # Check if the new file name already exists
    counter = 1
    base, extension = os.path.splitext(new_filename)
    while os.path.exists(new_file):
        new_file = os.path.join(directory, f"{base}_{counter}{extension}")
        counter += 1
    
    # Rename the file
    os.rename(old_file, new_file)
    print(f'Renamed: {filename} to {new_file}')

print("Renaming completed.")
