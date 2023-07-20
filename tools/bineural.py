import numpy as np
import wave
import struct
from audio_generator import AudioGenerator

# Frequency definitions
# Delta - Sleep - (0.5-4 Hz): 100-400 Hz - Frequency difference between the two tones can be around 1-4 Hz; tones typically in the range of 100-400 Hz.
# Theta - Meditation -  (4-8 Hz): 200-400 Hz - Frequency difference between the two tones can be around 4-8 Hz; tones typically in the range of 200-400 Hz.
# Alpha - Relaxation - (8-12 Hz): 200-500 Hz - Frequency difference between the two tones can be around 8-12 Hz; tones typically in the range of 200-500 Hz.
# Beta - Alertness - (12-30 Hz): 300-1000 Hz - Frequency difference between the two tones can be around 12-30 Hz; tones typically in the range of 300-1000 Hz.
# Gamma - Peak Focus - (30-100 Hz): 500-2000 Hz - Frequency difference between the two tones can be around 30-100 Hz; tones typically in the range of 500-2000 Hz.
# Focus 1: Associated with physical relaxation and release of tension. This state may be associated with alpha brainwave frequency range (8-12 Hz) or theta brainwave frequency range (4-8 Hz).
# Focus 2: Associated with increased awareness and visualization. This state may be associated with alpha brainwave frequency range (8-12 Hz) or theta brainwave frequency range (4-8 Hz).
# Focus 3: Associated with expanded awareness and a sense of detachment from physical sensations. This state may be associated with theta brainwave frequency range (4-8 Hz) or delta brainwave frequency range (0.5-4 Hz).
# Focus 10: Associated with the "mind awake/body asleep" state and a sense of detachment from physical sensations. This state may be associated with theta brainwave frequency range (4-8 Hz) or delta brainwave frequency range (0.5-4 Hz).
# Focus 12: Associated with heightened states of awareness and expanded consciousness. This state may be associated with gamma brainwave frequency range (30-100 Hz) or higher frequencies.
# Focus 15: Associated with the state of "no time" and a sense of being beyond physical reality. This state may be associated with delta brainwave frequency range (0.5-4 Hz) or theta brainwave frequency range (4-8 Hz).
# Focus 21: Associated with advanced states of consciousness and communication with higher intelligence. This state may be associated with gamma brainwave frequency range (30-100 Hz) or higher frequencies.


# Presets for brain states
presets = {
    "0_delta": {
        "freq_default": 300, # (100, 400)
        "binaural_default": 2.5, # (1, 4),
    },
    "1_theta": {
        "freq_default": 300, # (200, 400)
        "binaural_default": 4, # (4, 8),
    },
    "2_alpha": {
        "freq_default": 300, # (200, 500)
        "binaural_default": 8, # (8, 12),
    },
    "3_beta": {
        "freq_default": 300, # (300, 1000)
        "binaural_default": 12, # (12, 30),
    },
    "4_gamma": {
        "freq_default": 300, # (500, 2000)
        "binaural_default": 30, # (30, 100),
    }
}
presets_background = {
    "_pink": {
        "freq_default": 300, # (500, 2000)
        "binaural_default": 30, # (30, 100),
    },
}

def create_binaural_audio(preset, duration, save_path, gradual_freq_change=None, volume=1.0):
    chosen_preset = {}
    
    print("Creating binaural audio")
    print("preset tester")
    if (preset == "delta"):
        print("preset test")
        chosen_preset = "0_delta"
        print("preset changed")
    elif (preset == "theta"):
        print("preset test")
        chosen_preset = "1_theta"
        print("preset changed")
    elif (preset == "alpha"):
        print("preset test")
        chosen_preset = "2_alpha"
        print("preset changed")
    elif (preset == "beta"):
        print("preset test")
        chosen_preset = "3_beta"
        print("preset changed")
    elif (preset == "gamma"):
        print("preset test")
        chosen_preset = "4_gamma"
        print("preset changed")
    elif (preset == "pink"):
        print("preset test")
        chosen_preset = "_pink"
        print("preset changed")
    elif (preset == "custom"):
        print("preset test")
        chosen_preset = "custom"
        print("preset changed")
    else:
        print("Preset error")
        return False
        


###Tell me something That's not been said before That is paradoxical but true

    print("Creating binaural audio - 0")
    print(f"Chosen preset equals {chosen_preset}")
    freq_default = presets[chosen_preset]["freq_default"]
    freq_default = presets[chosen_preset]["freq_default"]
    binaural_default = presets[chosen_preset]["binaural_default"]
    entrainment_type = "binaural"
    sound_type = "sine"
    print("Creating binaural audio - 1")
    audio_gen = AudioGenerator()
    print("Creating binaural audio - 2")
    print(f"save_path = {save_path}")

    #save_path = r"\\THE-DOCTOR\website\complete audio\output.wav"  # Updated save_path

    audio_gen.generate_audio(
        save_path,
        duration,
        False, #fade in/out
        sound_type,
        freq_default,
        binaural_default,
        entrainment_type,
        volume_generator=None,
        gradual_freq_change=None,
        volume=volume
    )
    print("Creating binaural audio - 3")
    return save_path

def create_background_audio(preset, duration, save_path, volume=1.0):
    freq_default = preset["freq_default"]
    binaural_default = preset["binaural_default"]
    sound_type = "pink"

    audio_gen = AudioGenerator()
    audio_gen.generate_audio(
        save_path,
        duration,
        False, #fade in/out
        sound_type,
        freq_default,
        binaural_default,
        entrainment_type=None,
        volume_generator=None,
        gradual_freq_change=None,
        volume=volume
    )

def merge_audio_files(input_file1, input_file2, output_file):
    print("Start")
    with wave.open(input_file1, "rb") as f1, wave.open(input_file2, "rb") as f2:
        print("Opened Files")
        samp_width1 = f1.getsampwidth()
        samp_width2 = f2.getsampwidth()
        print(f"Sample Widths: {samp_width1} {samp_width2}")
        assert samp_width1 == samp_width2

        framerate1 = f1.getframerate()
        framerate2 = f2.getframerate()
        print(f"Frame Rates: {framerate1} {framerate2}")
        assert framerate1 == framerate2

        n_frames1 = f1.getnframes()
        n_frames2 = f2.getnframes()
        print(f"Number of Frames: {n_frames1} {n_frames2}")



        assert abs(n_frames1 - n_frames2) <= 1

        #assert n_frames1 == n_frames2

        n_channels1 = f1.getnchannels()
        n_channels2 = f2.getnchannels()
        print(f"Number of Channels: {n_channels1} {n_channels2}")
        n_channels = max(n_channels1, n_channels2)

        samp_width = samp_width1
        framerate = framerate1
        #n_frames = n_frames1
        n_frames = min(n_frames1, n_frames2)  # Update this line


        audio_data1 = np.frombuffer(f1.readframes(n_frames), dtype=np.int16).reshape(-1, n_channels1)
        audio_data2 = np.frombuffer(f2.readframes(n_frames), dtype=np.int16).reshape(-1, n_channels2)
        print("Read Audio Data")

        if n_channels1 < n_channels:
            audio_data1 = np.column_stack([audio_data1] + [np.zeros_like(audio_data1[:, 0])] * (n_channels - n_channels1))
            print("Adjusted Audio Data 1")

        if n_channels2 < n_channels:
            audio_data2 = np.column_stack([audio_data2] + [np.zeros_like(audio_data2[:, 0])] * (n_channels - n_channels2))
            print("Adjusted Audio Data 2")

        audio_data_combined = audio_data1 + audio_data2
        audio_data_combined = np.clip(audio_data_combined, -32768, 32767).astype(np.int16)
        print("Combined and Clipped Audio Data")

    with wave.open(output_file, "wb") as outf:
        outf.setnchannels(n_channels)
        outf.setsampwidth(samp_width)
        outf.setframerate(framerate)
        outf.writeframes(audio_data_combined.tobytes())
        print("Saved Output File")


    
if __name__ == '__main__':
    duration = 10  # in seconds
    
    output_folder = r'D:/Bambi AI/0_deleteables/binaural_audio_playground/output/'
    # Gradual frequency change (optional): specify the ear ("left" or "right"), the final frequency, and the duration of the change in seconds
    gradual_freq_change = None  # Example: ("left", 280, 5)

    output_file = f"{output_folder}pink_background.wav"
    create_background_audio(presets_background["_pink"], duration, output_file, volume=0.1)

    for preset in presets.keys():
        output_file = f"{output_folder}preset_{preset}.wav"
        create_binaural_audio(preset, duration, output_file, gradual_freq_change, volume=0.1)
        
    background_file = f"{output_folder}pink_background.wav"
    for preset in presets.keys():
            in_file = f"{output_folder}preset_{preset}.wav"
            out_file = f"{output_folder}preset_{preset}_pink_background.wav"
            merge_audio_files(in_file, background_file, out_file)
