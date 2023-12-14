
# https://github.com/SomeName2/audio-entrainment-python/blob/main/generate.py
import os
import wave
import numpy as np
import sys
import io
import tempfile
import traceback


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



   


    def generate_audio_data(self, duration, fade, sound_type, base_freq, binaural_freq_diff, entrainment_type, volume_generator, gradual_freq_change, volume):
        print("Generating audio data")
        print("duration: " + duration)
  
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

        if fade:
            ramp_length = int(sample_rate * 0.5)
            self.fade_in_out(audio_data, ramp_length)

        # Scale the audio array by the given volume
        audio_data *= volume

        return audio_data

    def convert_segments_to_wav_files(self, input_data):
        wav_file_paths = []
        temp_dir = tempfile.mkdtemp()  # Create a temporary directory
        
        # Determine the total number of frames in all segments
        
        for i, segment in enumerate(input_data):
            # Convert segment to bytearray if it's not already
            if not isinstance(segment, bytearray):
                segment = bytearray(segment)

            # Define the file path
            file_path = os.path.join(temp_dir, f"segment_{i}.wav")
            wav_file_paths.append(file_path)
        
            # Calculate the number of frames for this segment
            num_frames = len(segment) // (2 * 2)  # Assuming 16-bit stereo audio
            print(f"Segment {i}: Original frames: {num_frames}")
            
            # Set parameters for the WAV file
            num_channels = 2  # Mono=1, Stereo=2
            sample_width = 2  # 2 bytes (16 bits) per sample
            sample_rate = 44100  # Sampling frequency in Hz
            num_frames = len(segment) // (num_channels * sample_width)

            # Save the segment as a WAV file
            with wave.open(file_path, 'wb') as wav_file:
                wav_file.setnchannels(num_channels)
                wav_file.setsampwidth(sample_width)
                wav_file.setframerate(sample_rate)
                wav_file.setnframes(num_frames)
                wav_file.writeframes(segment)

        return wav_file_paths

    def combine_audio_segments(self, input_data, combined_file_path, save_path):
        print("~~~~save_path: " + save_path)
    
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
            wav_file_paths = self.convert_segments_to_wav_files(input_data)
            print("test5")

            # Process each WAV file
            for file_path in wav_file_paths:
                with wave.open(file_path, 'rb') as wav_file:
                    print("test6")
                    if not params:
                        params = wav_file.getparams()
                        print("test7")
                    combined_audio_data.extend(wav_file.readframes(wav_file.getnframes()))
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