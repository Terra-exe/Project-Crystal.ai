import os
import re
from pydub import AudioSegment

# Change this to your desired audio
audio_name = "Crystal serenity"

def extract_number(f):
    s = re.findall("\d+",f)
    return (int(s[0]) if s else -1,f)

# Directory where your .wav files reside
dir_name = f'\\\\server\\Magnum Opus\\dump\\audio\\{audio_name}_dump'

# Get list of all files
list_of_files = os.listdir(dir_name)

# Only consider .wav files
wav_files = [f for f in list_of_files if f.endswith('.wav') and f.startswith(f'genfile_{audio_name}')]

# Sort files numerically
wav_files.sort(key=extract_number)

combined_audio = AudioSegment.empty()


# Loop through files and append to combined_audio
for i, wav_file in enumerate(wav_files, start=1):
    print(f'Processing file {i} of {len(wav_files)}: {wav_file}')
    combined_audio += AudioSegment.from_wav(os.path.join(dir_name, wav_file))

# Set the new frame rate
new_frame_rate = 44100
combined_audio = combined_audio.set_frame_rate(new_frame_rate)

# Output file
out_dir = f'X:\\website\\tools\\audio_dump'
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, f'{audio_name}_combined_44100.wav')

# Export combined_audio to out_file
print(f'Exporting combined audio to {out_file}')
combined_audio.export(out_file, format='wav')
print('Done.')
