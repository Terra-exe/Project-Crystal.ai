import os
from pydub import AudioSegment

# Define source and destination directories
source_dir = r"D:\Bambi Videos\Refined\2024\March\Crystal Glaum\fix"
dest_dir = r"D:\Bambi Videos\Refined\2024\March\Crystal Glaum\fix\fixed"

# Ensure the destination directory exists
os.makedirs(dest_dir, exist_ok=True)

# Process each .wav file in the source directory
for filename in os.listdir(source_dir):
    if filename.endswith(".wav"):
        # Construct full path to source file
        filepath = os.path.join(source_dir, filename)
        
        # Load the audio file
        audio = AudioSegment.from_wav(filepath)
        
        # Increase volume by 7 dB
        audio = audio 
        
        # Convert to stereo by duplicating the mono track
        stereo_audio = AudioSegment.from_mono_audiosegments(audio, audio)
        
        # Construct full path to destination file
        dest_filepath = os.path.join(dest_dir, filename)
        
        # Export the modified audio file to the destination directory
        stereo_audio.export(dest_filepath, format="wav")

print("Processing complete.")
