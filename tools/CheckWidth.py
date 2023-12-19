from pydub import AudioSegment
import os

folder_path = 'X:\Project-Crystal.ai\sound_effects'  # Replace with the path to your folder

for filename in os.listdir(folder_path):
    if filename.endswith(".mp3") or filename.endswith(".wav"):  # Add other file extensions if needed
        audio = AudioSegment.from_file(os.path.join(folder_path, filename))
        print(f'File: {filename}, Sample Width: {audio.sample_width}')
