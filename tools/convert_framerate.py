from pydub import AudioSegment

def resample_audio(input_path, output_path, new_frame_rate):
    audio = AudioSegment.from_wav(input_path)
    audio = audio.set_frame_rate(new_frame_rate)
    audio.export(output_path, format="wav")

if __name__ == "__main__":
    input_path = "\\\\server\\Magnum Opus\\dump\\audio\\Crystal serenity_dump\\combined\\Crystal serenity_combined.wav"
    output_path = "X:\\website\\tools\\audio_dump\\Crystal serenity_combined_44100.wav"
    new_frame_rate = 44100
    resample_audio(input_path, output_path, new_frame_rate)