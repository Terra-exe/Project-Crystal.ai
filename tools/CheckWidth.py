from pydub import AudioSegment
import os

folder_path = 'X:\Project-Crystal.ai\sound_effects'  # Replace with the path to your folder


from pydub import AudioSegment
import os

folder_path = 'X:/Project-Crystal.ai/sound_effects'  # Replace with the path to your folder

for filename in os.listdir(folder_path):
    if filename.endswith(".mp3") or filename.endswith(".wav"):  # Add other file extensions if needed
        file_path = os.path.join(folder_path, filename)
        audio = AudioSegment.from_file(file_path)

        # Check if the frame rate is 44800 Hz
        if audio.frame_rate == 44800:
            # Convert frame rate to 44100 Hz
            audio_44100 = audio.set_frame_rate(44100)

            # Export the converted audio
            new_file_path = os.path.join(folder_path, "converted_44100_" + filename)
            audio_44100.export(new_file_path, format=filename.split('.')[-1])

            print(f'Converted: {filename} to 44100 Hz')
        else:
            print(f'File: {filename}, Sample Width: {audio.sample_width}, Frame Rate: {audio.frame_rate}')


for filename in os.listdir(folder_path):
    if filename.endswith(".mp3") or filename.endswith(".wav"):  # Add other file extensions if needed
        file_path = os.path.join(folder_path, filename)
        audio = AudioSegment.from_file(file_path)
        print(f'File: {filename}, Sample Width: {audio.sample_width}')

        if audio.sample_width != 2:
            # Export with a sample width of 2
            # Note: This may not produce the desired results as it's a complex conversion
            audio.set_sample_width(2).export(file_path, format="wav")
            print(f'File: {filename}, Sample Width: {audio.sample_width}')

