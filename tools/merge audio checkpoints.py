import os
import glob
from pydub import AudioSegment

WORKING_DIR = r'V:\Magnum Opus\dump\audio\Project Crystal 3_dump'
# Define the directory path where the audio files are located
audio_dir = WORKING_DIR

# Get a list of all the audio files in the directory
audio_files = glob.glob(os.path.join(audio_dir, 'checkpoint_*.wav'))

# Sort the audio files based on their number part
audio_files.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0].split('_')[-1]))

# Create an empty audio segment
combined_audio = AudioSegment.silent(duration=0)

# Track the progress of merging
total_files = len(audio_files)
current_file = 1

# Loop through each audio file, load it, and append it to the combined audio
for audio_file in audio_files:
    audio_segment = AudioSegment.from_wav(audio_file)
    combined_audio += audio_segment
    
    # Display the progress
    print(f"Merging file {current_file} of {total_files}")
    current_file += 1

# Define the output directory and file name for the combined audio file
output_dir = WORKING_DIR + '\combined'
output_file = os.path.join(output_dir, 'combined_audio.wav')

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Export the combined audio to the output file
combined_audio.export(output_file, format='wav')

print(f"The audio files have been merged and saved to {output_file}")
