
import pythoncom
import wave
import os
import pyttsx3
import io
import sys
#sys.path.append(r"C:\python server\website\json_builder\bin")
#sys.path.append(r"D:\audios")
sys.path.insert(1, r'\\SERVER\python server\website\json_builder\bin')
sys.path.insert(2, r'\\SERVER\python server\website')
sys.path.insert(3, r'\\SERVER\d\audios')
print(sys.path)
import kriya_object
import json
import time
from pydub import AudioSegment


VOICE_NAME = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\IVONA 2 Voice Salli22"
#VOICE_NAME = "en-us"
#VOICE_NAME = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'



#AUDIO_FOLDER_PATH = r"C:\python server\website\TTS\audios"
AUDIO_FOLDER_PATH = r"\\server\d\audios"
os.makedirs(AUDIO_FOLDER_PATH, exist_ok=True)

def speak(phrase):
    engine = pyttsx3.init()
    engine.setProperty('voice', VOICE_NAME)
    #rate = engine.getProperty('rate')
    #engine.setProperty('rate', int(rate * 0.60))
    engine.say(phrase)
    engine.runAndWait()
    engine.stop()

def create_audio_file_single_phrase(filename, jsondata):
    print("running")
    pythoncom.CoInitialize()  # initialize the COM library
    
    engine = pyttsx3.init()
    engine.setProperty('voice', VOICE_NAME)
    #rate = engine.getProperty('rate')
    # Save the audio file to the same directory as the script
    try:
        # Create a new .wav file and write the audio data to it
        engine.save_to_file(jsondata["step1"], os.path.join(AUDIO_FOLDER_PATH, filename + '.wav'))
        #print('Audio file saved successfully')
    except Exception as e:
        print(f'Error saving audio file: {e}')
        return None
    
    print("waiting")
    engine.runAndWait()

    while not os.path.exists(os.path.join(AUDIO_FOLDER_PATH, filename + '.wav')):
        # Wait until the file is fully saved
        time.sleep(0.1)

    # Check the file size to ensure it's fully saved
    file_size = 0
    while file_size < os.path.getsize(os.path.join(AUDIO_FOLDER_PATH, filename + '.wav')):
        file_size = os.path.getsize(os.path.join(AUDIO_FOLDER_PATH, filename + '.wav'))
        time.sleep(0.1)
    
    print('Audio file saved successfully')    

    
    # Clean up resources
    print("stopping")
    engine.stop()
    
    engine = None  # remove the reference to the engine instance
    pythoncom.CoUninitialize()  # uninitialize the COM library
    
    print("returning")
    return f"{filename}.wav"



'''
##########
##########
##########
It creates all the audio files except for the last audio file. So that needs to be fixed.
Also it's converting the sub steps that have wait times associated with them into text which is wrong.
Also it might be a good idea to convert the Json into an object properly so that I don't have to use these strange arrays with zero in them
Maybe I should define the format and then ask chat GPT to convert it into a new format for me from the old.
##########
##########
##########
'''
def json_to_audio(jsondata): 
    #jdata = json.load(jsondata)

    print("running")
    
    pythoncom.CoInitialize()  # initialize the COM library
    
    engine = pyttsx3.init()
    engine.setProperty('voice', VOICE_NAME)
    #print(jsondata["title"])
    #print(jsondata)
    engine.setProperty('rate', 150) # set the speed to 150 wpm
    #engine.setProperty('rate', engine.getProperty('rate') - 50) # slow down by 50 wpm


    kriya_obj = None

    try:
        kriya_obj = kriya_object.create_kriya_obj_from_json(jsondata)
        ##kriya.print_kriya()
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")

    filename = kriya_obj.title.replace(".json", "")
    print("\n---\n")


    audio_segments = []
    i = 1


    for e_array_counter, e_array in enumerate(kriya_obj.kriya, start=1):

        #kriya_segment_filename = f"{filename}_kriya_{e_array.exercise}.wav"
        #print(kriya_segment_filename)
        #print(e_array.exercise)

        for e_counter, exercise in enumerate(e_array.steps, start=1):
            #print(f"\tExercise:")
            for s_counter, substep in enumerate(exercise.substeps, start=1):
                for ss_counter, (key, value) in enumerate(substep.__dict__.items(), start=1): 
                    if (type(value) == str):
                        #print(f"\t\t\t{key}: {value} this is substep{ss_counter} text")
                        try:
                            #print(AUDIO_FOLDER_PATH)
                            print("value = " + value)

                            segment_filename = f"genfile_{filename}_{i}.wav"
                            
                            engine.save_to_file(value, os.path.join(AUDIO_FOLDER_PATH, segment_filename))
                            engine.runAndWait()
                            time.sleep(0.1) # this might be worth removing
                            spoken_segment = AudioSegment.from_wav(os.path.join(AUDIO_FOLDER_PATH, segment_filename))
                            #print(AUDIO_FOLDER_PATH)
                            #print("value = " + value)
                            i+=1
                            audio_segments.append(spoken_segment)
                        except Exception as e:
                            print(f'Error saving audio file: {e}')
                            return None 


                    elif (isinstance(value, dict) and \
                        (value['type'] == "pauseMedium" or value['type'] == "pauseShort" or value['type'] == "waitLong" or value['type'] == "breakLong")):
                        #print(f"\t\t\t{key}: {value} this is substep{ss_counter} wait object")
                        ss_silence_segment = AudioSegment.silent(duration=int(float(value['value']) * 1000))
                        engine.runAndWait()
                        audio_segments.append(ss_silence_segment)

            if hasattr(e_array, 'wait'):
                for wait in e_array.wait:
                    #print(f"\t\tWait: {wait.value}{wait.timeframe} ({wait.type} - {wait.description}) this is a substep_group{e_array_counter} wait object")
                    silence_segment = AudioSegment.silent(duration=int(float(wait.value) * 1000))
                    engine.runAndWait()
                    audio_segments.append(silence_segment)
    
    print("---Combining---")
    #result_segment = os.system(f"ffmpeg -i \"concat:{'|'.join(audio_segments)}\" -acodec copy {filename}.wav")
    #engine.runAndWait()
    #result_segment.export("result.wav", format="wav")

    # concatenate all the audio segments into a single audio file
    combined_audio = AudioSegment.empty()
    for segment in audio_segments:
        combined_audio = combined_audio + segment
    combined_audio.export(os.path.join(AUDIO_FOLDER_PATH, f"{filename}_combined.wav"), format="wav")
    
    engine.runAndWait() 
    
   # print("Hello4")
    # delete the audio segments
    print("---Deleting---")
    for i, segment in enumerate(audio_segments, start=1):
        try:
            os.remove(os.path.join(AUDIO_FOLDER_PATH, f"genfile_{filename}_{i}.wav"))
        except:
            pass

   
    # Clean up resources
    print("stopping")
    engine.stop()
    
    engine = None  # remove the reference to the engine instance
    pythoncom.CoUninitialize()  # uninitialize the COM library
    
    print("returning")


    return f"{filename}.wav"

def get_audio_folder_path():
    return AUDIO_FOLDER_PATH

def get_audio_by_name(filename): ##currently innactive
    return AUDIO_FOLDER_PATH + "\\" +  filename

