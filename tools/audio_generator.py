
# https://github.com/SomeName2/audio-entrainment-python/blob/main/generate.py
import os
import wave
import numpy as np
import sys
import io
import tempfile
import traceback
from pydub import AudioSegment
from pydub.generators import Sine
#from scipy.io import wavfile



class AudioGenerator:
    def __init__(self):
        self.sound_generators = {
            "sine": self.gen_sine,
            "square": self.gen_square,
            "triangle": self.gen_triangle,
            "smooth_square": self.gen_smooth_square,
            "white": self.gen_white,
            "pink": self.gen_pink,
            "brown": self.gen_brown,
        }
        self.entrainment_generators = {
            "binaural": self.gen_binaural,
            "monoural": self.gen_monoural,
            "isochronic": self.gen_isochronic,
            "none": self.gen_none,
        }
        self.sample_rate = 44100  # Sample rate in Hz



    def generate_audio(
        self,
        save_path,
        title,
        duration,
        do_fade_in_out,
        sound_type,
        freq=None,
        binaural=None,
        entrainment_type=None,
        volume_generator=None,
        gradual_freq_change=None,
        volume=0.5):
    
        print("Creating binaural audio - 4")

        sample_rate = 44100
        noise_generators = set({"white", "pink", "brown"})
        print("Creating binaural audio - 5")
        try:
            if sound_type in noise_generators:
                sound_freq = 1
                beat_freq = None
                print("Creating binaural audio - 6")
                if entrainment_type is None:
                    entrainment_type = "none"
                else:
                    entrainment_type = "isochronic"
                    beat_freq = freq
                    volume_generator = self.sound_generators[volume_generator]
            else:
                print("Creating binaural audio - 7")
                sound_freq = freq

                if entrainment_type is None:
                    entrainment_type = "none"
                    beat_freq = None
                else:
                    beat_freq = binaural

                    if entrainment_type == "isochronic":
                        volume_generator = self.sound_generators[volume_generator]

            sound_generator = self.sound_generators[sound_type]
            entrainment_generator = self.entrainment_generators[entrainment_type]
        except:
            traceback.print_exc()
        print("Creating binaural audio - 8")
        if entrainment_type == "isochronic":
            print("Creating binaural audio - 8.1")
            arr = entrainment_generator(
                sound_freq, beat_freq, sample_rate, duration, sound_generator, volume_generator
            )
            print("Creating binaural audio - 8.2")
        else:
            print("Creating binaural audio - 8.3")
            try:
                print("sound_freq:", sound_freq)
                print("beat_freq:", beat_freq)
                print("sample_rate:", sample_rate)
                print("duration:", duration)

                arr = entrainment_generator(
                    sound_freq, beat_freq, sample_rate, duration, sound_generator
                )
                print("Creating binaural audio - 8.3.1")
            except Exception as e:
                print(f"Error encountered: {e}")

            print("Creating binaural audio - 8.4")
        print("Creating binaural audio - 11")
        ramp_length = int(sample_rate * 0.5)

        if do_fade_in_out:
            self.fade_in_out(arr, ramp_length)

        # Scale the audio array by the given volume
        arr *= volume
        print("Creating binaural audio - 9")

        if not os.path.isdir(save_path):
            print(f"Directory '{save_path}' not found. Creating it now...")
            os.makedirs(save_path)
        else:
            print(f"Directory '{save_path}' already exists.")

        self.save_wav(save_path + title, arr, sample_rate)

        print("Creating binaural audio - 10")
        print("Saved here: " + save_path + title)






    def generate_gradual_audio(self, start_preset, mid_preset, end_preset, duration, save_path, title, do_fade_in_out, sound_type, freq=None, binaural=None, entrainment_type=None, volume_generator=None, gradual_freq_change=None, volume=0.5):
        """
        Generate a customizable binaural beat audio file.

        This function allows you to create a binaural audio file with gradual frequency changes over its duration. The generated audio file will be saved as a WAV file.

        :param start_preset: The brainwave state preset for the beginning of the audio (e.g., 'delta', 'theta', 'alpha').
        :param mid_preset: The brainwave state preset for the middle portion of the audio.
        :param end_preset: The brainwave state preset for the end of the audio.
        :param duration: The duration of the generated audio in seconds.
        :param save_path: The file path where the generated audio will be saved as a WAV file.
        :param title: A descriptive title for the audio file.
        :param do_fade_in_out: A boolean flag indicating whether to apply fade-in and fade-out effects to the audio.
        :param sound_type: The type of sound to be generated (e.g., 'binaural', 'monaural', 'isochronic').
        :param freq: Optional - the base frequency (in Hz) for the binaural beat. If not provided, it will be determined by the selected presets.
        :param binaural: Optional - the binaural frequency difference (in Hz) for the binaural beat. If not provided, it will be determined by the selected presets.
        :param entrainment_type: Optional - the type of brainwave entrainment (e.g., 'binaural', 'monaural', 'isochronic').
        :param volume_generator: Optional - a function that generates volume envelopes or modulations for the audio.
        :param gradual_freq_change: Optional - a parameter indicating how the frequency of the right ear should gradually change over time.
        :param volume: Optional - the overall volume level of the generated audio (0.0 to 1.0).

        This function will create a single binaural audio file with the specified duration, starting with the frequencies defined by the 'start_preset' and gradually transitioning to the frequencies defined by the 'mid_preset' and 'end_preset'. The right ear's frequency will smoothly change from the starting to the ending frequency over the course of the audio.

        You can also customize the audio with fade-in and fade-out effects, select the sound type, fine-tune the base frequency and binaural difference, and apply volume modulation for a more tailored brainwave entrainment experience.

        Once generated and saved as a WAV file, this audio can be used for meditation, relaxation, or any other purpose that benefits from brainwave entrainment techniques.
        """
        
        ###

        """
        Instructions, Cautions, Recommendations, Notes, and Advice for GPT
        Parameter Validation: It's good to have validations for input parameters like start_preset, mid_preset, and end_preset to ensure they are within your defined presets. 
        Also, validate duration to be positive and check if save_path and title are valid strings.
        
        Frequency Transition: For the gradual frequency change (Step 5), you've used linear interpolation (np.linspace). 
        #This is fine for a basic implementation, but consider if you need more complex transitions (like exponential or custom curves).

        Audio File Saving:

        Make sure you correctly combine left_channel and right_channel into a stereo audio format.
        Set the parameters (like sample rate, format, etc.) correctly in the wave.open method.
        You might need to convert the NumPy arrays to a format suitable for WAV files, typically 16-bit integers.

        Testing and Error Handling: Include error handling for potential issues (file writing errors, invalid parameters, etc.). Using print statements will help track issues.
        
        Performance Considerations: If performance is a concern, especially for long durations, 

        """
        presets = {
            "0_delta": {
                "freq_default": 256, # (100, 400)
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
            }
        }

        preset_mapping = {
            'delta': '0_delta',
            'theta': '1_theta',
            'alpha': '2_alpha',
            'beta': '3_beta',
            'gamma': '4_gamma',
            'root': '5_root',
            'sacral': '6_sacral',
            'solar': '7_solar',
            'heart': '8_heart',
            'throat': '9_throat',
            '3rdeye': '10_3rdeye',
            'crown': '11_crown'
        }

        start_preset = preset_mapping[start_preset]
        mid_preset = preset_mapping[mid_preset]
        end_preset = preset_mapping[end_preset]
        print("Presets loaded...")

        # Frequencies for the left ear
        start_left_freq = presets[start_preset]["freq_default"]  # Frequency for the left ear at the start
        mid_left_freq = presets[mid_preset]["freq_default"]      # Frequency for the left ear in the middle
        end_left_freq = presets[end_preset]["freq_default"]      # Frequency for the left ear at the end

        # Frequencies for the right ear
        # These frequencies will gradually change over the duration of the binaural beat
        start_right_freq = presets[start_preset]["binaural_default"] + start_left_freq  # Starting frequency for the right ear
        mid_right_freq = presets[mid_preset]["binaural_default"] + mid_left_freq      # Middle frequency for the right ear
        end_right_freq = presets[end_preset]["binaural_default"] + end_left_freq      # Ending frequency for the right ear

        
        
        print("Starting generate_gradual_audio function...")
        
        #Generate a customizable binaural beat audio file.

        # Step 1: Set up the audio generation parameters
        # Define a variable named num_samples and calculate it by multiplying the duration (in seconds) by the sample_rate (already set to 44100).
        sample_rate = 44100  # Standard sample rate for audio files
        # Parameter Validation: 
        # Check if the duration is a positive number
        if duration <= 0:
            print("Duration must be a positive number.")
            return
        # confirm that the presets (start_preset, mid_preset, end_preset) are valid.
        if start_preset not in presets or mid_preset not in presets or end_preset not in presets:
            print("Invalid presets.")
            return
        
        # Step 2: Calculate the number of audio samples based on the duration
        # Calculate the total number of audio samples and store it in the num_samples variable.
        num_samples = int(duration * sample_rate)  # Calculate the total number of samples
        
        # Step 3: Create arrays to store audio data for both left and right channels
        # Initialize two NumPy arrays: left_channel and right_channel with zeros as placeholders. These arrays will hold the audio data for the left and right channels.
        """Implementation:
            Import the NumPy library.
            Initialize two arrays, left_channel and right_channel, with zeros. The size of these arrays should be equal to num_samples.
            """
        left_channel = np.zeros(num_samples)
        right_channel = np.zeros(num_samples)
        # Memory Considerations: For very long durations and high sample rates, these arrays can become quite large. If you anticipate generating very long audio files, you might want to consider strategies to manage memory usage, such as processing the audio in chunks.
        print("Left and right audio channels initialized.")
    
        # Step 4: Create time values for the audio
        # This time array is essential for audio signal generation. It represents each point in time within the audio track.
        # We will use it to calculate the value of the sine wave at each sample point, thereby creating the audio signal.
        # 'numpy.linspace' is used to generate evenly spaced time values from 0 to the duration of the audio, corresponding to the number of samples.
        time = np.linspace(0, duration, num_samples)
        # add a check to ensure the time array is generated as expected. confirming its length matches num_samples
        if len(time) != num_samples:
            print("Error: The length of the time array does not match the number of samples.")
            return
        else:
            print("Time array generated successfully.")
        # Optimization Consideration: If you later find that performance is an issue (especially with very long durations), you might consider strategies to optimize this part.

        # Step 5: Generate the gradual frequency change for the right ear
        # Based on your specific requirements, calculate how the frequency for the right ear should gradually change over time. Store this information in an array named right_freq_change.
        # Determine the method for calculating the frequency change (linear, exponential, etc.).
        # Store the calculated frequency changes in an array named right_freq_change using linear interpolation for frequency change
        right_freq_change = np.linspace(start_right_freq, end_right_freq, num_samples)  
        
        # Consider Alternative Transition Methods: While linear interpolation is a solid choice, in some cases, you might want to offer different types of transitions (e.g., logarithmic, exponential). This could be beneficial for different types of auditory experiences or brainwave entrainment effects. However, this is more of an enhancement than a necessity.
        # Linear interpolation is chosen in your code for generating the gradual frequency change primarily due to its simplicity and effectiveness in creating a smooth and steady transition between two values over a specified interval
        # Validation of Frequency Values: 
        # Ensure that the frequency values (start_right_freq, mid_right_freq, end_right_freq) are within 20 Hz to 20 kHz
        if start_right_freq < 20 or start_right_freq > 20000 or mid_right_freq < 20 or mid_right_freq > 20000 or end_right_freq < 20 or end_right_freq > 20000:
            print("Frequency values must be between 20 Hz and 20 kHz.")
            return
        # It's important to keep these frequencies within the limits of human hearing (typically 20 Hz to 20 kHz) and also within the limits of the audio file format (typically 44.1 kHz for WAV files).
        print("Gradual frequency change for the right ear generated successfully.")


        # Step 6: Generate the audio data using vectorized operations
        left_freq = start_left_freq  # Assuming a constant frequency for the left channel

        # Calculate the sine wave for the left channel (constant frequency)
        # Using vectorized operations for efficient computation
        left_channel = np.sin(2 * np.pi * left_freq * time)

        # Calculate the sine wave for the right channel (variable frequency)
        # The frequency for the right ear is dynamically adjusted based on the right_freq_change array
        right_channel = np.sin(2 * np.pi * right_freq_change * time)

        # Optionally, apply volume modulation
        # Volume modulation can be applied either through a provided volume_generator function or a fixed volume level
        if volume_generator is not None:
            # The volume_generator should provide a volume envelope to modulate the audio dynamically
            volume_envelope = volume_generator(num_samples)
            left_channel *= volume_envelope
            right_channel *= volume_envelope
        elif volume != 1.0:
            # Apply a fixed volume factor to both channels
            left_channel *= volume
            right_channel *= volume
        print("Audio data generation complete.")
        # Considerations for Audio Amplitude
        # It's important to ensure that the amplitude of the sine waves is set at an appropriate level to avoid clipping
        # while also ensuring the audio is loud enough to be heard clearly. This might involve normalizing the audio or
        # adjusting the volume parameters to maintain the desired loudness and clarity.



        # Step 7: Open a WAV file for writing and Write the audio data to the file, create the folder if it doesn't exist
        # Ensure the directory exists
        print("save_path created :  " + save_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            print(f"Folder '{save_path}' created.")
        else:
            print(f"Folder '{save_path}' already exists.")
        
        # Open the WAV file for writing
        # self.save_wav(save_path + title...)
        file_path = os.path.join(save_path, title + '.wav')
        with wave.open(file_path, 'w') as wav_file:
            # Set parameters for the WAV file
            # It's crucial to set all necessary parameters in the wave.open method correctly.
            # This includes the number of channels (2 for stereo), sample width (often 16 bits for standard WAV files),
            # and frame rate (equal to your sample_rate).
            n_channels = 2
            sampwidth = 2  # 2 bytes (16 bits) for standard WAV files
            wav_file.setparams((n_channels, sampwidth, sample_rate, num_samples, 'NONE', 'not compressed'))
        
            # Data Format Conversion: Convert the floating-point values to 16-bit integers
            # The data in your NumPy arrays (left_channel and right_channel) should be converted to a format suitable for WAV files, typically 16-bit PCM.
            # This involves normalizing and converting the floating-point values in your arrays to 16-bit integers.
            max_amplitude = 32767  # Maximum amplitude for 16-bit audio
            left_channel_int = (left_channel * max_amplitude).astype(np.int16)
            right_channel_int = (right_channel * max_amplitude).astype(np.int16)

            # Combining Channels: Interleave the left and right channel data for stereo output
            # This can be done by alternating samples from each channel or using a suitable library function.
            stereo_data = np.vstack((left_channel_int, right_channel_int)).T.flatten()
            
            # Write audio data to the WAV file
            wav_file.writeframes(stereo_data.tostring())

            print("Audio data written to", file_path)
            # Error Handling: The context manager (with statement) and the error handling in the libraries used (wave, os)
            # should manage most file-related errors. However, additional specific error handling for your application's needs
            # could be implemented to manage cases where the file may not be writable due to permissions or other issues.

            # Resource Management: The use of a context manager (with statement) for file operations ensures that the file is
            # properly closed after writing, even if an error occurs. This is important for preventing resource leaks and ensuring data integrity.



    '''
    def generate_gradual_audio(self, start_preset, mid_preset, end_preset, duration, save_path, title, do_fade_in_out, sound_type, freq=None, binaural=None, entrainment_type=None, volume_generator=None, gradual_freq_change=None, volume=1.0):
    #def generate_gradual_audio(self, start_preset, mid_preset, end_preset, duration, save_path, title):
        print("Starting generate_gradual_audio function...")

        sample_rate = 44100  # standard sample rate for audio files

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

        preset_mapping = {
            'delta': '0_delta',
            'theta': '1_theta',
            'alpha': '2_alpha',
            'beta': '3_beta',
            'gamma': '4_gamma'
        }

        start_preset = preset_mapping[start_preset]
        mid_preset = preset_mapping[mid_preset]
        end_preset = preset_mapping[end_preset]
        print("Presets loaded...")

        start_freq = presets[start_preset]["freq_default"]
        mid_freq = presets[mid_preset]["freq_default"]
        end_freq = presets[end_preset]["freq_default"]

        start_binaural = presets[start_preset]["binaural_default"]
        mid_binaural = presets[mid_preset]["binaural_default"]
        end_binaural = presets[end_preset]["binaural_default"]
        

        print("Preset frequencies and binaural values loaded...")

        total_samples = int(duration * sample_rate)
        arr = np.zeros((2, total_samples))

        print("Initialized audio array...")
        beat_freq = binaural
        
        try:
            if sound_type in self.sound_generators:
                sound_freq = 1
                if entrainment_type is None:
                    entrainment_type = "none"
                else:
                    entrainment_type = "isochronic"
        
                    volume_generator = self.sound_generators[volume_generator]
            else:
                sound_freq = freq_default
                if entrainment_type is None:
                    entrainment_type = "none"
                    beat_freq = None
                else:
                    beat_freq = binaural
                    if entrainment_type == "isochronic":
                        volume_generator = self.sound_generators[volume_generator]

            sound_generator = self.sound_generators[sound_type]
            entrainment_generator = self.entrainment_generators[entrainment_type]
        except:
            traceback.print_exc()


        for sample in range(total_samples):
            current_time = sample / sample_rate

            if current_time < duration / 2:
                
                current_freq = np.interp(current_time, [0, duration / 2], [start_freq + start_binaural, mid_freq + mid_binaural])
            else:
                current_freq = np.interp(current_time, [duration / 2, duration], [mid_freq + mid_binaural, end_freq + end_binaural])

            arr[0, sample] = np.sin(2 * np.pi * current_time * start_freq)  # left ear
            arr[1, sample] = np.sin(2 * np.pi * current_time * current_freq)  # right ear
            if sample % 10000 == 0:  # print progress every 10000 samples
                print(f"Processed {sample} samples...")
        



        print("Audio generation complete...")
        print("save_path : " + save_path)
        print("title : " + title)
        
        #Ensure the directory exists
        print("save_path created... :  " + save_path)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            print(f"Folder '{save_path}' created.")
        else:
            print(f"Folder '{save_path}' already exists.")
        
        #self.save_wav(r"/tmp/audios-draft-v1/variable_frequency/aa_ONLY_variable_frequency_delta_alpha_theta.wav", arr, sample_rate)   
        self.save_wav(save_path + title, arr, sample_rate)
        print("Audio saved.")'''


    def gen_x(self, duration, sample_rate, freq):
        return np.linspace(0, duration * freq - freq / sample_rate, int(duration * sample_rate))

    def gen_sine(self, x):
        return np.sin(x * 2 * np.pi)

    def gen_square(self, x):
        return np.round(x - np.floor(x), 0) * 2 - 1

    def gen_triangle(self, x):
        return np.abs(x - np.floor(x) - 0.5) * 4 - 1

    def gen_smooth_square(self, x):
        y = self.gen_triangle(x) * 7
        y[y > 1] = 1
        y[y < -1] = -1

        return y

    def fft_noise(self, scales):
        n = scales.shape[0]

        phases = np.random.rand(n) * 2 * np.pi
        phases = np.cos(phases) + 1j * np.sin(phases)
        phases *= scales

        res = np.zeros((n + 1) * 2, dtype=complex)

        res[1:1 + n] = phases
        res[-1:-1 - n:-1] = np.conj(phases)

        res = np.fft.ifft(res).real

        return res / np.abs(res).max()

    def gen_white(self, x):
        return np.random.rand(x.shape[0]) * 2 - 1

    def gen_pink(self, x):
        dur = x[1] * x.shape[0]
        n = (x.shape[0] - 2) // 2

        scales = 1 / np.sqrt(np.fft.fftfreq(x.shape[0], x[1])[1:1 + n])
        scales[:int(16 * dur)] = 0

        return self.fft_noise(scales)

    def gen_brown(self, x):
        dur = x[1] * x.shape[0]
        n = (x.shape[0] - 2) // 2

        scales = 1 / np.fft.fftfreq(x.shape[0], x[1])[1:1 + n]
        scales[:int(16 * dur)] = 0

        return self.fft_noise(scales)


    def fade_in_out(self, arr, ramp_length):
        ramp = np.linspace(0, 1, ramp_length)

        if len(arr.shape) == 2:
            ramp = ramp[:, None]

        arr[:ramp_length] *= ramp

        ramp = ramp[::-1]
        arr[-ramp_length:] *= ramp

    def gen_binaural(self, sound_freq, beat_freq, sample_rate, duration, tone_generator):
        diff = beat_freq / 2
        l_x = self.gen_x(duration, sample_rate, sound_freq - diff)
        r_x = self.gen_x(duration, sample_rate, sound_freq + diff)

        l_y = tone_generator(l_x)
        r_y = tone_generator(r_x)

        ramp_length = int(sample_rate * 0.5)

        y = np.concatenate((l_y[:, None], r_y[:, None]), 1)

        return y

    def gen_monoural(self, sound_freq, beat_freq, sample_rate, duration, tone_generator):
        diff = beat_freq / 2
        x_1 = self.gen_x(duration, sample_rate, sound_freq - diff)
        x_2 = self.gen_x(duration, sample_rate, sound_freq + diff)

        y = (tone_generator(x_1) + tone_generator(x_2)) / 2

        return y

    def gen_none(self, sound_freq, beat_freq, sample_rate, duration, tone_generator):
        x = self.gen_x(duration, sample_rate, sound_freq)

        y = tone_generator(x)

        return y

    def gen_isochronic(self, sound_freq, beat_freq, sample_rate, duration, tone_generator, volume_generator):
        x_1 = self.gen_x(duration, sample_rate, sound_freq)
        x_2 = self.gen_x(duration, sample_rate, beat_freq)

        y_1 = tone_generator(x_1)
        y_2 = volume_generator(x_2) / 2 + 0.5

        y = y_1 * y_2

        return y

    def save_wav(self, path, arr, sample_rate):
        arr *= np.iinfo(np.int16).max
        arr = arr.astype(np.int16)

        with wave.open(path, "wb") as f:
            f.setnchannels(len(arr.shape))
            f.setsampwidth(2)
            f.setframerate(sample_rate)

            f.writeframes(arr)