import numpy as np
import wave
import struct
import os
from .audio_generator import AudioGenerator

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
    },
    "5_root": {
        "freq_default": 252 , # Associated Frequency: 256 Hz
        "binaural_default": 8, # (4, 8),
    },
    "6_sacral": {
        "freq_default": 283.5, # Associated Frequency: 288 Hz
        "binaural_default": 9, # (8, 12),
    },
    "7_solar": {
        "freq_default": 314.5, #  Associated Frequency: 320 Hz
        "binaural_default": 11, # (12, 30),
    },
    "8_heart": {
        "freq_default": 335.3, # Associated Frequency: 341.3 Hz
        "binaural_default": 12, # (30, 100),
    },
    "9_throat": {
        "freq_default": 378, # Associated Frequency: 384 Hz
        "binaural_default": 12.5, # (30, 100),
    },
    "10_3rdeye": {
        "freq_default": 420.2, # Associated Frequency: 426.7 Hz
        "binaural_default": 13, # (30, 100),
    },
    "11_crown": {
        "freq_default": 472.5, # Associated Frequency: 480 Hz
        "binaural_default": 15, # (30, 100),
    },
    "12_none": {
        "freq_default": 0,
        "binaural_default": 0,
    }

}
presets_background = {
    "_pink": {
        "freq_default": 300, # (500, 2000)
        "binaural_default": 30, # (30, 100),
    },
}

def create_binaural_audio(preset, duration, save_path, title, gradual_freq_change=None, volume=0.5, start_preset=None, mid_preset=None, end_preset=None):
    chosen_preset = {}
    
    print("Creating binaural audio")
    print("preset tester")
    if (preset == "delta"):
         
        chosen_preset = "0_delta"
         
    elif (preset == "theta"):
         
        chosen_preset = "1_theta"
         
    elif (preset == "alpha"):
         
        chosen_preset = "2_alpha"
         
    elif (preset == "beta"):
         
        chosen_preset = "3_beta"
         
    elif (preset == "gamma"):
         
        chosen_preset = "4_gamma"
         
    elif (preset == "pink"):
         
        chosen_preset = "_pink"
         
    elif (preset == "root"):
         
        chosen_preset = "5_root"
           
    elif (preset == "sacral"):
         
        chosen_preset = "6_sacral"
         
    elif (preset == "solar"):
         
        chosen_preset = "7_solar"
         
    elif (preset == "heart"):
         
        chosen_preset = "8_heart"
             
    elif (preset == "throat"):
         
        chosen_preset = "9_throat"
         
    elif (preset == "3rdeye"):
         
        chosen_preset = "10_3rdeye"
         
    elif (preset == "crown"):
         
        chosen_preset = "11_crown"
                       
    elif (preset == "custom"):
         
        chosen_preset = "custom"
         
    elif (preset == "none"):
        chosen_preset = "none"
         
    elif (preset == "variable_frequency"):
        print("Preset variable_frequency")
        chosen_preset = "variable_frequency" 
        freq_default = None 
        binaural_default = None
    else:
        print("Preset error")
        return False
    
    print("Creating binaural audio - 0")
    print(f"Chosen preset equals {chosen_preset}")
    if (chosen_preset != "variable_frequency"):
        
        freq_default = presets[chosen_preset]["freq_default"]
        freq_default = presets[chosen_preset]["freq_default"]
        binaural_default = presets[chosen_preset]["binaural_default"]

    if (chosen_preset != "none"):  
        entrainment_type = "binaural"
        sound_type = "sine"

        print("Creating binaural audio - 1")
        audio_gen = AudioGenerator()
        print("Creating binaural audio - 2")
        print(f"save_path = {save_path}{title}")

    
        if gradual_freq_change:
            # Call generate_gradual_audio if gradual_freq_change is True
            # You need to provide start_preset, mid_preset, and end_preset
            print(" audio_gen.generate_gradual_audio(start_preset, mid_preset, end_preset, duration, save_path, title")
            audio_gen.generate_gradual_audio(
                start_preset,
                mid_preset,
                end_preset,
                duration,
                save_path,
                title,
                False, #fade in/out
                sound_type,
                freq_default,
                binaural_default,
                entrainment_type,
                volume_generator=None,
                gradual_freq_change=True,
                volume=volume
            )
        else:
            audio_gen.generate_audio(
                save_path,
                title,
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


def get_preset_from_frequency_name(freq_name):
    # Map the frequency name to the corresponding preset key
    preset_map = {
        "delta": "0_delta",
        "theta": "1_theta",
        "alpha": "2_alpha",
        "beta": "3_beta",
        "gamma": "4_gamma",
        "root": "5_root",
        "sacral": "6_sacral",
        "solar": "7_solar",
        "heart": "8_heart",
        "throat": "9_throat",
        "3rdeye": "10_3rdeye",
        "crown": "11_crown"
    }
    return presets.get(preset_map.get(freq_name, None), None)









'''
In this function:
We use linear interpolation to calculate the frequency at each point in time.
The duration is assumed to be in a unit that matches the time increment used in the loop (e.g., seconds).
The actual generation of binaural beats (generate_binaural_beat) will depend on your existing setup and is represented here as a placeholder.
'''
'''
def generate_variable_frequency_binaural(preset, start_freq, mid_freq, end_freq, duration, save_path, title, gradual_freq_change=True, volume=1.0):
    print(f"Received preset: {preset}")
    print(f"Start frequency: {start_freq}")
    print(f"Mid frequency: {mid_freq}")
    print(f"End frequency: {end_freq}")
    print(f"Duration: {duration}")
    print(f"Save path: {save_path}")
    print(f"Title: {title}")
    print(f"Gradual freq change: {gradual_freq_change}")
    print(f"Volume: {volume}")
        
    # Inside your route or function where you call generate_variable_frequency_binaural
    start_preset = get_preset_from_frequency_name(start_freq)
    mid_preset = get_preset_from_frequency_name(mid_freq)
    end_preset = get_preset_from_frequency_name(end_freq)
   

    # Make sure the directory exists
    segment_dir = os.path.join(save_path, title)
    if not os.path.exists(segment_dir):
        os.makedirs(segment_dir)

    # Linear interpolation function
    def interpolate(freq_start, freq_end, time_start, time_end, current_time):
        print(f"Interpolating from {freq_start} to {freq_end} between times {time_start} and {time_end} at current time {current_time}")
        return freq_start + (freq_end - freq_start) * (current_time - time_start) / (time_end - time_start)

    # Calculate mid-point of the duration
    mid_point = duration / 2
    print(f"Mid point: {mid_point}")

    # Initialize AudioGenerator
    audio_gen = AudioGenerator()


    # Initialize a list to hold audio data of each segment
    combined_audio_data = []
    
    # Number of full second segments
    num_full_segments = int(duration)



    # Process each full second segment
    for current_time in range(num_full_segments):
        if current_time <= mid_point:
            base_freq = interpolate(start_preset["freq_default"], mid_preset["freq_default"], 0, mid_point, current_time)
            binaural_freq = interpolate(start_preset["freq_default"] + start_preset["binaural_default"], 
                                        mid_preset["freq_default"] + mid_preset["binaural_default"], 
                                        0, mid_point, current_time)
        else:
            base_freq = interpolate(mid_preset["freq_default"], end_preset["freq_default"], mid_point, duration, current_time)
            binaural_freq = interpolate(mid_preset["freq_default"] + mid_preset["binaural_default"], 
                                        end_preset["freq_default"] + end_preset["binaural_default"], 
                                        mid_point, duration, current_time)

        segment_data = audio_gen.generate_audio_data(1, False, "sine", base_freq, binaural_freq - base_freq, "binaural", None, False, volume)
        #print(f"!!!XXX!!!Number of frames in segment_data!!!XXX!!!: {len(segment_data) // (2 * 2)}")

        combined_audio_data.append(segment_data)

    # Handle fractional part if present
    fractional_part = duration - num_full_segments
    if fractional_part > 0:
        final_time = duration
        if final_time <= mid_point:
            base_freq = interpolate(start_preset["freq_default"], mid_preset["freq_default"], 0, mid_point, final_time)
            binaural_freq = interpolate(start_preset["freq_default"] + start_preset["binaural_default"], 
                                        mid_preset["freq_default"] + mid_preset["binaural_default"], 
                                        0, mid_point, final_time)
        else:
            base_freq = interpolate(mid_preset["freq_default"], end_preset["freq_default"], mid_point, duration, final_time)
            binaural_freq = interpolate(mid_preset["freq_default"] + mid_preset["binaural_default"], 
                                        end_preset["freq_default"] + end_preset["binaural_default"], 
                                        mid_point, duration, final_time)

        final_segment_data = audio_gen.generate_audio_data(fractional_part, False, "sine", base_freq, binaural_freq - base_freq, "binaural", None, False, volume)
        combined_audio_data.append(final_segment_data)

    # Combine all segments and save as a single file
    combined_file_path = title
    
    print(f"Combined File Path: {combined_file_path}")

# Since combined_audio_data is a list of audio data segments, it should be passed directly to combine_audio_segments

    audio_gen.combine_audio_segments(combined_audio_data, combined_file_path, save_path)




    return combined_file_path     ''' 



def create_background_audio(preset, duration, save_path, volume=0.5):
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

def print_wav_properties(filepath):
    with wave.open(filepath, "rb") as wav_file:
        print("Channels:", wav_file.getnchannels())
        print("Sample width:", wav_file.getsampwidth())
        print("Frame rate (frames/sec):", wav_file.getframerate())
        print("Number of frames:", wav_file.getnframes())
        print("Compression type:", wav_file.getcomptype())
        print("Compression name:", wav_file.getcompname())

def merge_audio_files(input_file1, input_file2, output_file):
    print("Start")
    print("Input 1 - input_file1: \n")
    print_wav_properties(input_file1)
    print("Input 2 - input_file2: \n")
    print_wav_properties(input_file2)


    
    with wave.open(input_file1, "rb") as f1, wave.open(input_file2, "rb") as f2:
        n_channels1 = f1.getnchannels()
        n_channels2 = f2.getnchannels()

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


        print("frames1")
        if n_frames2 >= 2 * n_frames1:
            # Read and process the second audio file to be half the number of frames as the first one
            audio_data2 = np.frombuffer(f2.readframes(n_frames2 // 2), dtype=np.int16).reshape(-1, n_channels2)
        elif n_frames2 != n_frames1:
            # If n_frames2 is not equal to n_frames1 and not exactly double, handle it as needed
            # You can choose how to handle this situation, such as skipping frames or truncating.
            # Here, we skip the extra frames in n_frames2 to match n_frames1.
            #print("Read Framess??? " + str(f2.readframes(n_frames2 - n_frames1)))
            pass
        
        print("Uhh:  " + str(n_frames1 ))

        print("Uhh:  " + str(n_frames2 ))

         # Calculate and print the duration for both audio files
        duration1 = n_frames1 / framerate1
        duration2 = n_frames2 / framerate2
        print(f"Duration of Input 1: {duration1:.2f} seconds")
        print(f"Duration of Input 2: {duration2:.2f} seconds")

        assert abs(n_frames1 - n_frames2) <= 1

        #assert n_frames1 == n_frames2
        print("frames4")        
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


'''
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
'''