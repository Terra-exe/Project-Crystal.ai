import os
import ffmpeg
from pydub import AudioSegment
import speech_recognition as sr
import nltk

# Download the NLTK list of vulgar words if not already downloaded
nltk.download('punkt')

# Define the word to censor
censor_word = "cock"

def censor_audio(audio_segment):
    recognizer = sr.Recognizer()
    
    # Save the AudioSegment to a temporary WAV file
    temp_wav_path = "temp_audio.wav"
    audio_segment.export(temp_wav_path, format="wav")
    
    # Convert audio to text
    with sr.AudioFile(temp_wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return audio_segment
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            return audio_segment

    # Split text into words
    words = nltk.word_tokenize(text)
    
    # Find and censor the specified word
    beep = AudioSegment.sine(frequency=1000, duration=500)
    censored_audio = AudioSegment.empty()
    current_position = 0

    for word in words:
        word_start = text.find(word, current_position)
        word_end = word_start + len(word)
        
        # Add the audio segment before the word
        censored_audio += audio_segment[current_position * 1000 // len(text) : word_start * 1000 // len(text)]
        
        if word.lower() == censor_word.lower():
            # Add beep for the specified word
            censored_audio += beep
        else:
            # Add the original word audio
            censored_audio += audio_segment[word_start * 1000 // len(text) : word_end * 1000 // len(text)]
        
        current_position = word_end
    
    # Add remaining part of the audio
    censored_audio += audio_segment[current_position * 1000 // len(text):]
    
    # Remove temporary file
    os.remove(temp_wav_path)
    
    return censored_audio

def extract_audio(input_video_path, output_audio_path):
    try:
        ffmpeg.input(input_video_path).output(output_audio_path).run(overwrite_output=True)
    except Exception as e:
        print(f"Error extracting audio: {e}")

def reattach_audio(input_video_path, input_audio_path, output_video_path):
    try:
        # Reattach the censored audio to the video using ffmpeg
        ffmpeg.input(input_video_path).input(input_audio_path).output(output_video_path, vcodec='copy', acodec='aac').run(overwrite_output=True)
    except Exception as e:
        print(f"Error reattaching audio: {e}")

def censor_video(input_video_path, output_video_path):
    temp_audio_path = "temp_audio.wav"
    censored_audio_path = "censored_audio.wav"
    
    extract_audio(input_video_path, temp_audio_path)
    
    try:
        # Load audio segment and censor it
        audio_segment = AudioSegment.from_file(temp_audio_path)
        censored_audio_segment = censor_audio(audio_segment)
        
        # Save censored audio to a new file
        censored_audio_segment.export(censored_audio_path, format="wav")
        
        # Reattach the censored audio to the video
        reattach_audio(input_video_path, censored_audio_path, output_video_path)
    except Exception as e:
        print(f"Error processing or saving censored audio: {e}")
    finally:
        # Clean up temporary files
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        if os.path.exists(censored_audio_path):
            os.remove(censored_audio_path)

# Example usage
input_video_path = r"D:\Bambi Videos\Refined\2024\May\Bambi's Hookup Fantasy\Complete\Bambi's Hookup Fantasy v7 (soft ending - audio only).mp4"
output_video_path = r"D:\Bambi Videos\Refined\2024\May\Bambi's Hookup Fantasy\Complete\Bambi's Hookup Fantasy v7 (soft ending - audio only) censored.mp4"

censor_video(input_video_path, output_video_path)
