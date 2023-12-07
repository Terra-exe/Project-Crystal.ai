
# https://github.com/SomeName2/audio-entrainment-python/blob/main/generate.py
import os
import wave
import numpy as np
import sys
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