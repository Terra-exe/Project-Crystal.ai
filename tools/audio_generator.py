
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
        volume=1.0):
    
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



    def generate_audio_data(self, duration, base_freq, binaural_freq, volume):
        """
        Generate a segment of binaural audio.

        :param duration: Duration of the audio segment in seconds
        :param base_freq: Frequency for the left ear in Hz
        :param binaural_freq: Frequency for the right ear in Hz
        :param volume: Volume of the audio, range from 0.0 to 1.0
        :return: AudioSegment object representing the binaural audio
        """
        print("Generating binaural audio segment...")
        print(f"Duration: {duration} seconds")
        print(f"Base frequency (left ear): {base_freq} Hz")
        print(f"Binaural frequency (right ear): {binaural_freq} Hz")
        print(f"Volume: {volume}")
        # Check if base_freq is too high
        if base_freq > 32767:
            print("Base frequency is too high, reducing to 32767 Hz")
            base_freq = 32767


        # Check if volume is too high
        if volume > 1.0:
            print("Volume is too high, reducing to 1.0")
            volume = 1.0

        # Scale the volume to the expected range
        scaled_volume = volume * 100

        # Convert duration from seconds to milliseconds
        duration_ms = duration * 1000

        # Generate sine wave for left ear
        print("Generating sine wave for left ear...")
        print(f"Base frequency: {base_freq}")
        print(f"Duration: {duration_ms} ms")
        print(f"Scaled volume: {scaled_volume}")

        left_channel = Sine(base_freq).to_audio_segment(duration=duration_ms, volume=volume)

        # Generate sine wave for right ear with the binaural frequency
        print("Generating sine wave for right ear...")
        right_channel = Sine(binaural_freq).to_audio_segment(duration=duration_ms, volume=volume)

        # Combine into a stereo audio segment
        print("Combining left and right channels into stereo audio...")
        stereo_audio = AudioSegment.from_mono_audiosegments(left_channel, right_channel)

        print(f"Generated audio data with base frequency {base_freq} Hz and binaural frequency {binaural_freq} Hz")
        return stereo_audio


    '''
    def generate_audio_data(self, duration, fade, sound_type, base_freq, binaural_freq_diff, entrainment_type, volume_generator, gradual_freq_change, volume):
        print("Generating audio data")
        print("duration: " + str(duration))
  
        sample_rate = 44100
        noise_generators = {"white", "pink", "brown"}
        audio_data = []

        try:
            if sound_type in noise_generators:
                sound_freq = 1
                beat_freq = None
                if entrainment_type is None:
                    entrainment_type = "none"
                else:
                    entrainment_type = "isochronic"
                    beat_freq = base_freq
                    volume_generator = self.sound_generators[volume_generator]
            else:
                sound_freq = base_freq
                beat_freq = base_freq + binaural_freq_diff
                if entrainment_type != "isochronic":
                    entrainment_type = "none"

            sound_generator = self.sound_generators[sound_type]
            entrainment_generator = self.entrainment_generators[entrainment_type]
        except:
            traceback.print_exc()

        if entrainment_type == "isochronic":
            audio_data = entrainment_generator(
                sound_freq, beat_freq, sample_rate, duration, sound_generator, volume_generator
            )
        else:
            audio_data = entrainment_generator(
                sound_freq, beat_freq, sample_rate, duration, sound_generator
            )

        #if fade:
        #    ramp_length = int(sample_rate * 0.5)
        #    self.fade_in_out(audio_data, ramp_length)

        # Scale the audio array by the given volume
        audio_data *= volume
        #print("YYYXXX!!!Number of frames in audio data:YYYXXX!!!", len(audio_data))

        return audio_data'''
    '''
    def convert_segments_to_wav_files(self, input_data):
         # Print the number of frames for each segment in input_data
        for i, segment in enumerate(input_data):
            num_frames = len(segment)  # Assuming segment is a NumPy array or similar
            print(f"Initial Segment {i}: Number of frames: {num_frames}")

        wav_file_paths = []
        temp_dir = tempfile.mkdtemp()  # Create a temporary directory
        
        # Determine the total number of frames in all segments
        
        for i, segment in enumerate(input_data):
            # Print length before conversion to bytearray
            print(f"Segment {i} length before bytearray conversion: {len(segment)}")

        

            # Print length after conversion to bytearray
            print(f"Segment {i} length after bytearray conversion: {len(segment)}")

            # Define the file path
            file_path = os.path.join(temp_dir, f"segment_{i}.wav")
            wav_file_paths.append(file_path)
            

           

            
            #num_frames = len(segment) // (2 * 2)  # Assuming 16-bit stereo audio
            #print(f"Segment {i}: len // 2 * 2 frames: {num_frames}")
            
            # Set parameters for the WAV file
            num_channels = 2  # Mono=1, Stereo=2
            sample_width = 2  # 2 bytes (16 bits) per sample
            sample_rate = 44100  # Sampling frequency in Hz
            #num_frames = len(segment) // (num_channels * sample_width)

            num_frames = len(segment)  # Calculate the number of frames
            print(f"ZZZZZZNumber of frames in segment {i}: {num_frames}")

            print("XXXX FRAMES XXX :" + str(num_frames))
            # Save the segment as a WAV file
            with wave.open(file_path, 'wb') as wav_file:
                wav_file.setnchannels(num_channels)
                wav_file.setsampwidth(sample_width)
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(segment)

            with wave.open(file_path, "rb") as f1:
                print("~~~Opened Files")
                samp_width1 = f1.getsampwidth()
                print(f"~~~Sample Widths: {samp_width1} ")
                

                framerate1 = f1.getframerate()
                print(f"~~~Frame Rates: {framerate1} ")


                n_frames1 = f1.getnframes()
                print(f"~~~Number of Frames: {n_frames1} ")

                
        return wav_file_paths
        '''



    def combine_audio_segments(self, segments, output_path):
        """
        Combine a list of audio segments into a single audio file.

        :param segments: List of AudioSegment objects
        :param output_path: Path to save the combined audio file
        """
        print("Combining audio segments...")

        # Check if there are segments to combine
        if not segments:
            print("No audio segments provided.")
            return

        # Initialize a new audio segment for combining
        combined_segment = AudioSegment.silent(duration=0)

        # Iterate and combine each segment
        for i, segment in enumerate(segments):
            print(f"Adding segment {i + 1}/{len(segments)} to the combined audio...")
            combined_segment += segment

        print(f"Total duration of combined audio: {len(combined_segment) / 1000.0} seconds")

        # Export combined audio to the specified file path
        print(f"Exporting combined audio to {output_path}...")
        combined_segment.export(output_path, format="wav")

        print(f"Combined audio file saved at: {output_path}")

# Example usage
# audio_gen = AudioGenerator()
# combined_audio = audio_gen.combine_audio_segments(audio_segments, "path/to/output.wav")

    '''def combine_audio_segments(self, input_data, combined_file_path, save_path):
        print("~~~~save_path: " + save_path)

        # Construct the full file path
        full_file_path = os.path.join(save_path, combined_file_path.lstrip('/'))
        # Create the directory if it does not exist
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        if not full_file_path.endswith('.wav'):
            raise ValueError("The full_file_path should be a .wav file path, not a directory.")

        # Check if a directory with the same name exists
        if os.path.isdir(full_file_path):
            raise ValueError(f"A directory with the name {full_file_path} already exists.")

        # Initialize variables for combined audio data
        combined_audio_data = []
        params = None

        # Check if input_data is a directory path
        if isinstance(input_data, (str, bytes, os.PathLike)) and os.path.isdir(input_data):
            # List all segment files in the directory and sort them
            segment_files = sorted(os.listdir(input_data))
            print("test2")
            # Iterate over and combine each segment file
            for file in segment_files:
                with wave.open(os.path.join(input_data, file), 'rb') as segment:
                    # Read and append audio data
                    combined_audio_data.extend(segment.readframes(segment.getnframes()))
                    if not params:
                        params = segment.getparams()
            print("test3")

        elif isinstance(input_data, list) and input_data:
            print("test4")
            # Combine raw audio data segments
            for i, segment in enumerate(input_data):
                segment_array = np.array(segment, dtype=np.int16)
                combined_audio_data.extend(segment_array)                
                if not params:
                    # Here, set your audio parameters based on how you handle the audio data
                    # For example, if all segments are 44100 Hz, 16-bit, stereo:
                    num_channels = 2
                    sample_width = 2  # 2 bytes per sample (16 bit)
                    sample_rate = 44100
                    params = (num_channels, sample_width, sample_rate, 0, 'NONE', 'not compressed')
               
                # Calculate and print the duration for each segment
                num_frames = len(segment_array) // (num_channels * sample_width)  # Correct frame count for stereo
                segment_duration = num_frames / sample_rate  # Duration in seconds
                #print(f"Raw Segment {i}: Number of frames: {num_frames}, Duration: {segment_duration:.2f} seconds")


            print("test5")

        else:
            raise ValueError("Invalid input. Must be a directory path or a list of audio data segments.")

        
        # Convert combined_audio_data to a bytearray if it's not already
        if not isinstance(combined_audio_data, bytearray):
            print("test5.1")
            combined_audio_data = bytearray(np.array(combined_audio_data, dtype=np.int16).tobytes())

        # Save combined audio data to combined_file_path
        if not params:
            raise ValueError("Audio parameters could not be determined. Please check input data.")
        print("test9")
        with wave.open(full_file_path, 'wb') as output_file:
            output_file.setparams(params)
            output_file.writeframes(combined_audio_data)
                # Reopen the file in read mode to get the number of frames
        with wave.open(full_file_path, 'rb') as read_file:
            frame_count = read_file.getnframes()
            print(f"...........Number of frames in the combined file:.......... {frame_count}")

        print("test10")'''



    """
    def combine_audio_segments(self, input_data, combined_file_path, save_path):
        print("~~~~save_path: " + save_path)
    
        # Iterate through each segment in input_data and print the number of frames
        for i, segment in enumerate(input_data):
            num_frames = len(segment)  # Get the number of frames in the segment
            print(f"-X-X-X-X-Segment {i}: Number of frames: {num_frames}")


        # Construct the full file path
        full_file_path = os.path.join(save_path, combined_file_path.lstrip('/'))
        # Create the directory if it does not exist
        os.makedirs(os.path.dirname(full_file_path), exist_ok=True)

        print(f"Arguments received: input_data={input_data}, full_file_path={full_file_path}")
        
        if not full_file_path.endswith('.wav'):
            raise ValueError("The full_file_path should be a .wav file path, not a directory.")

        # Check if a directory with the same name exists
        if os.path.isdir(full_file_path):
            raise ValueError(f"A directory with the name {full_file_path} already exists.")

        # Initialize variables for combined audio data
        combined_audio_data = bytearray()
        params = None
        print("test1")

        # Check if input_data is a directory path
        if isinstance(input_data, (str, bytes, os.PathLike)) and os.path.isdir(input_data):
            # List all segment files in the directory and sort them
            segment_files = sorted(os.listdir(input_data))
            print("test2")
            # Iterate over and combine each segment file
            for file in segment_files:
                with wave.open(os.path.join(input_data, file), 'rb') as segment:
                    # Read and append audio data
                    combined_audio_data.extend(segment.readframes(segment.getnframes()))
                    if not params:
                        params = segment.getparams()
            print("test3")
        
        elif isinstance(input_data, list) and input_data:
            print("test4")
             # Print the number of frames for each raw audio data in input_data
            for i, segment in enumerate(input_data):
                num_frames = len(segment)  # Assuming segment is a NumPy array or similar
                print(f"Raw Segment {i}: Number of frames: {num_frames}")


            wav_file_paths = self.convert_segments_to_wav_files(input_data)
            print("test5")

            # Process each WAV file
            for file_path in wav_file_paths:
                with wave.open(file_path, 'rb') as wav_file:
                    print("test6")
                    if not params:
                        params = wav_file.getparams()
                        print("test7")
                    print(" Try GetFrames of Segment!!!!" + str(wav_file.getnframes()))
                    combined_audio_data.extend(wav_file.readframes(wav_file.getnframes()))
                    print(" combined_audio_data Try GetFrames of Segment!!!!" + str(wav_file.getnframes()))

                    print("test8")
        else:
            raise ValueError("Invalid input. Must be a directory path or a list of audio data segments.")

        # Save combined audio data to combined_file_path
        if not params:
            raise ValueError("Audio parameters could not be determined. Please check input data.")
        print("test9")
        with wave.open(full_file_path, 'wb') as output_file:
            output_file.setparams(params)
            output_file.writeframes(combined_audio_data)
        print("test10")


    """

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