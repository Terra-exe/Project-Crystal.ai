#############
###IMPORTS###
#############
import sys
import os
import time
import socket
import requests
import contextlib
import json
import wave
import math
import io
import re
import boto3
import shutil
from botocore.exceptions import NoCredentialsError
from pydub.utils import mediainfo



from contextlib import closing
from io import BytesIO
from pydub import AudioSegment




#from flask import Flask
from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
import json_builder.bin.kriya_json_builder as kriya_json_builder
import json_builder.bin.kriya_object as kriya_object
import tools.bineural as bineural
import tools.youtube as youtube


##################
###MAIN GLOBALS###
##################

HOME_TITLE = r"Home"
APP5_TITLE = r"App5"
APP6_TITLE = r"App6"
APP7_TITLE = r"App7"
APP51_TITLE = r"App51"


APP5_DESCRIPTION = r"API Audio gen"
APP6_DESCRIPTION = r"Audio / Bineural Merge"
APP7_DESCRIPTION = r"Audio / to MP4 - Youtube Submit"
APP51_DESCRIPTION = r"Audio / Merge files, save to S3"


#from flask import Flask
app = Flask(__name__)


###########
###FLASK###
###########

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route("/" + APP5_TITLE.lower())
def app5():    
    context = {
            'app_title': APP5_TITLE + ' ' + APP5_DESCRIPTION,
            'app_header': APP5_TITLE + ' ' + APP5_DESCRIPTION,
            'form_action': '/submit_' + APP5_TITLE,
            'form_label': 'Enter text for ' + APP5_TITLE
        }
    return render_template(APP5_TITLE.lower() + ".php", context=context)

@app.route("/" + APP5_TITLE.lower() + "/audio/crystal_demo")
def api_serve_audio():
    # Create a boto3 client
    print("Button pressed.")

    s3 = boto3.client(
        's3',
        region_name='us-west-2',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )
    print("S3 connected.")

    # Replace 'your_bucket_name' and 'path/to/your/file.wav'
    # with your actual bucket name and file path inside the bucket
    bucket_name = 'project-crystal-public'
    key = 'audio/demo/voice demo/crystal_demo.wav'

    # Download the file from S3 into an in-memory bytes buffer
    file_obj = BytesIO()
    try:
        # Download the file from S3 into an in-memory bytes buffer
        s3.download_fileobj(bucket_name, key, file_obj)
    except Exception as e:
        print("An error occurred while downloading the file from S3: ", str(e))
        return jsonify(error="An error occurred while fetching the audio file."), 500


    # Serve the audio file
    file_obj.seek(0)  # Move file pointer back to the beginning of the file
    print("success demo button")
    return send_file(file_obj, mimetype='audio/wav')
    

    #return send_file(r'\\THE-DOCTOR\website\TTS\audios\demos\crystal_demo.wav', mimetype='audio/wav')


@app.route('/' + APP5_TITLE.lower() + '/create-audio-file', methods=['POST'])
def api_create_audio_file():

    # Path to audio-gen directory
    dir_path = "/tmp/audio-dumps/audio-gen-files"
    # Check if audio-gen directory exists, create one if not
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # Path to error file directory
    error_dir_path = "/tmp/audio-dumps/audio-gen-files"
    # Check if error file directory exists, create one if not
    if not os.path.exists(error_dir_path):
        os.makedirs(error_dir_path)

    input_json = {}
    
    print("\n\n---------GENERATING JSON---------\n\n")
    print("\n\n---------GENERATING JSON---------\n\n")
    print("\n\n---------GENERATING JSON---------\n\n")


    # Initialize clients for Polly and S3
    polly = boto3.client('polly', region_name='us-west-2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    s3 = boto3.client('s3', region_name='us-west-2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    bucket_name = 'crystal-audio-processing'
    s3_key = 'audio-dumps/audio-gen-files/Kriya.wav'
    s3_gen_file_key = r'audio-dumps/audio-gen-files/'
    s3_key_json = 'audio-dumps/audio-gen-files/json_input.json'
    s3_key_json_kriya = 'audio-dumps/audio-gen-files/json_kriya.json'
    s3_key_error = 'audio-dumps/audio-gen-files/error.txt'
    error_file_path = os.path.join("/tmp", s3_key_error)

    try:
        dir_path = "/tmp/audio-dumps/audio-gen-files"

        # Check if the directories exist, and create them if they do not
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)


        # Getting JSON data from the POST request
        input_json = request.get_json()
        
        # Save the JSON data to a file and upload the file to S3
        json_file_path = os.path.join("/tmp", s3_key_json)
        with open(json_file_path, 'w') as json_file:
            json.dump(input_json, json_file)

        # Upload JSON file to S3
        s3.upload_file(json_file_path, bucket_name, s3_key_json)


    except Exception as e1:
        with open(error_file_path, 'w') as error_file:
             error_file.write(str(e1))
        s3.upload_file(error_file_path, bucket_name, s3_key_error)
        print(f"Error saving JSON: {e1}")
        return jsonify({'message': f'Error saving JSON: {e1}'}), 500
    

    #Make sure jsondata is serializable
    jsondata = kriya_json_builder.kriya_webformat_to_json(input_json)
    
    # Save the JSON data to a file and upload the file to S3
    json_kriya_file_path = os.path.join("/tmp", s3_key_json_kriya)
    with open(json_kriya_file_path, 'w') as json_kriya_file:
        json.dump(jsondata, json_kriya_file)

    # Upload JSON file to S3
    s3.upload_file(json_file_path, bucket_name, s3_key_json_kriya)

    # Create Kriya object
    try:
        kriya_obj = kriya_object.create_kriya_obj_from_json(jsondata)
    except json.JSONDecodeError as e2:
        with open(error_file_path, 'w') as error_file:
            error_file.write(str(e2))
            s3.upload_file(error_file_path, bucket_name, s3_key_error)
            print(f"Error during Text-To-Speech: {e2}")
        return jsonify({'message': f'Error decoding JSON: {e2}'}), 400
    

    filename = kriya_obj.title.replace(".json", "")
    print("\n---\n")

    audio_segments = []
    i = 1

    # Get total expected files
    total_files = sum(1 for kriya in jsondata['kriya'] for step in kriya['steps'] for substep in step['substeps'] for key in substep if key.startswith("substep"))
    
    # Create a counter for created files
    created_files = 0
    print(f"Total files: 0 of {total_files}")
    print(f"Segment Creation Progress: {created_files / total_files * 100:.2f}%")

    checkpoint_counter = 1
    file_counter = 0


    for e_array_counter, e_array in enumerate(kriya_obj.kriya, start=1):
        for e_counter, exercise in enumerate(e_array.steps, start=1):
            for s_counter, substep in enumerate(exercise.substeps, start=1):
                for ss_counter, (key, value) in enumerate(substep.__dict__.items(), start=1):
                    # Is it a string?
                    if (type(value) == str): 
                        try:

                            value_cut = re.sub(r'[^a-zA-Z0-9\s]+', '', value[:50])
                            value_cut = re.sub(r'\s+', ' ', value_cut)

                            segment_filename = f"genfile_{filename}_{i}_#_{value_cut}.wav"
                            #segment_full_file_path = os.path.join(dump_dir_path, segment_filename)
                            
                            # Using Amazon Polly for text-to-speech, value = text
                            tts_and_save_to_s3(bucket_name, s3_gen_file_key + segment_filename, value)
                            # Increment counter
                            i+=1
                            created_files += 1
                            file_counter += 1 

                            # Print progress every 100 files
                            if created_files % 10 == 0:
                                print(f"Segment Creation Progress: {created_files / total_files * 100:.2f}%")

                            # This might be removable
                            if file_counter % 500 == 0:
                                checkpoint_counter += 1
                                file_counter = 0

                        except Exception as e4:
                            with open(error_file_path, 'w') as error_file:
                                error_file.write(str(e4))
                            s3.upload_file(error_file_path, bucket_name, s3_key_error)
                            print(f"Error during conversion to speech: {e4}")
                            return jsonify({'message': f'Error during conversion to speech: {e4}'}), 500
                    
                    elif (isinstance(value, dict) and \
                        (value['type'] == "pauseMedium" or value['type'] == "pauseShort" or value['type'] == "waitLong" or value['type'] == "breakLong")):
                        
                        silent_name = 'pause'
                        segment_filename_s3 = f"genfile_{filename}_{i}_#_{silent_name}.wav"
                        segment_filename_local = generate_silent_file(int(float(value['value']) * 1000), "/tmp/silence.wav")
                        upload_to_s3(bucket_name, s3_gen_file_key + segment_filename_s3, segment_filename_local)
                        i+=1
                    
                    elif (isinstance(value, dict) and \
                        (value['type'] == "soundEffect")):
                        
                        soundEffect_name = value['value']
                        segment_filename_s3 = f"genfile_{filename}_{i}_#_{soundEffect_name}.wav"
                        segment_filename_local = generate_silent_file(int(float(9) * 1000), "/tmp/silence.wav")
                        upload_to_s3(bucket_name, s3_gen_file_key + segment_filename_s3, segment_filename_local)
                        i+=1
            
            if hasattr(e_array, 'wait'):
                for wait in e_array.wait:
                    silent_name = 'pause'
                    segment_filename_s3 = f"genfile_{filename}_{i}_#_{silent_name}.wav"
                    segment_filename_local = generate_silent_file(int(float(wait.value) * 1000), "/tmp/silence.wav")
                    upload_to_s3(bucket_name, s3_gen_file_key + segment_filename_s3, segment_filename_local)
                    i+=1
                        


    # Use Amazon Polly to convert the text to speech
    try:
        response = polly.synthesize_speech(Text=kriya_obj.title, OutputFormat='pcm', VoiceId='Salli')
        
        
    except Exception as e3:
        with open(error_file_path, 'w') as error_file:
            error_file.write(str(e3))
        s3.upload_file(error_file_path, bucket_name, s3_key_error)
        print(f"Error during conversion to speech: {e3}")
        return jsonify({'message': f'Error during conversion to speech: {e3}'}), 500

    # If we have an audiostream in the response
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            pcm_data = stream.read()
            # Convert PCM to WAV using pydub
            sound = AudioSegment.from_raw(io.BytesIO(pcm_data), sample_width=2, channels=1, frame_rate=16000)
            # Convert the WAV data to bytes
            buffer = io.BytesIO()
            sound.export(buffer, format="wav")
            wav_data = buffer.getvalue()

            
            output = os.path.join("/tmp", s3_key)

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(wav_data)

            except IOError as ioe:
                print(ioe)
                print(f'Error: File {output} could not be written.')
                return jsonify({'message': f'Error: File {output} could not be written.'}), 500

            else:
                # upload the file to s3
                s3.upload_file(output, bucket_name, s3_key)
                print(f'File {output} uploaded to {bucket_name} at {s3_key}')

    return jsonify({'message': 'Success'})

# Step 1: Generate the silent segment
def generate_silent_file(duration_milliseconds, filename):
    silence = AudioSegment.silent(duration=duration_milliseconds)
    # Export to wav
    silence.export(filename, format="wav")
    return filename
    

# Step 2: Upload the silent segment to S3
def upload_to_s3(bucket_name, s3_key, file_path):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, s3_key)

def write_to_s3(bucket_name, s3_key, data):
    s3 = boto3.resource('s3')
    object = s3.Object(bucket_name, s3_key)
    object.put(Body=data)

def tts_and_save_to_s3(bucket_name, s3_key, text):
    polly_client = boto3.client('polly', region_name='us-west-2')
    response = polly_client.synthesize_speech(
                    VoiceId='Salli',
                    OutputFormat='pcm',
                    Text=text
                )
    # The response's 'AudioStream' body contains the audio data in the specified format
    pcm_data = response['AudioStream'].read()


    # Convert PCM to WAV using pydub
    sound = AudioSegment.from_raw(io.BytesIO(pcm_data), sample_width=2, channels=1, frame_rate=16000)
    # Resample the audio to 44.1 kHz
    sound = sound.set_frame_rate(44100)

    # Convert the WAV data to bytes
    buffer = io.BytesIO()
    sound.export(buffer, format="wav")
    wav_data = buffer.getvalue()

    # Save directly to an object in an S3 buckets
    write_to_s3(bucket_name, s3_key, wav_data)

def download_files_from_s3(bucket_name, key, title, download_dir='.', default_prefix=None):

    """
    Downloads audio files from an S3 bucket based on the provided title.

    :param bucket_name: Name of the S3 bucket
    :param title: Title used in the audio file naming
    :param download_dir: Directory to download files to (default is current directory)
    """
    print("download_files_from_s3()")
    

    # Check if the directory exists and create it if necessary
    print(f"2 Checking directory: {download_dir}")
    if not os.path.isdir(download_dir):
        print(f"Directory '{download_dir}' not found. Creating it now...")
        os.makedirs(download_dir)
    else:
        print(f"Directory '{download_dir}' already exists.")


    # Initialize the S3 client
    s3 = boto3.client('s3', region_name='us-west-2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

    print("\nKey is: ", key, "\n")
    # List objects in the bucket with a specific prefix
    prefix = ""
    if (default_prefix==None):
        prefix = key + f"genfile_{title}_" 
    else:
        prefix = key + title
    

    print(f"Searching in bucket: {bucket_name} for files with prefix: {prefix}")  # Print bucket and prefix info

    continuation_token = None
    while True:
        list_kwargs = {
            'Bucket': bucket_name,
            'Prefix': prefix,
        }
        if continuation_token:
            list_kwargs['ContinuationToken'] = continuation_token

        objects = s3.list_objects_v2(**list_kwargs)

        if 'Contents' not in objects:
            print("No files in bucket.")
            break

        # Filter files based on the title and naming pattern
        for obj in objects['Contents']: 
            if obj['Key'].endswith(".wav"):
                # Download the file
                local_filename = obj['Key'].split('/')[-1]  # Assuming the file is not inside a subdirectory in the bucket

                try:
                    s3.download_file(bucket_name, obj['Key'], os.path.join(download_dir, local_filename))
                    print(f"Downloaded {local_filename}")
                except Exception as e:
                    print(f"Failed to download {local_filename}. Error: {e}")
        
        continuation_token = objects.get('NextContinuationToken')
        if not continuation_token:
            break



def merge_audio_files(directory, title, output_directory):
    # List all files in the directory and filter them based on the naming pattern
    files = [f for f in os.listdir(directory) if f.startswith(f"genfile_{title}_") and f.endswith(".wav")]

    # Sort the files based on the sequence number
    files.sort(key=lambda f: int(f.split("_")[2]))

    # Create an empty audio segment to concatenate files to
    merged_audio = AudioSegment.empty()
  # Output file name
    output_file = os.path.join(output_directory, f"{title}_combined.wav")

    # Concatenate the audio files one by one
    for file in files:
        audio_path = os.path.join(directory, file)
        audio = AudioSegment.from_wav(audio_path)
       #print(f'File: {file} has {audio.channels} channel(s)')  # print channel number for each file
        print(f'File: {file} is merging into: {output_file} and it has {audio.channels} channel(s)')  # print channel number for each file


        merged_audio += audio

    # Export the merged audio to a new file
    merged_audio.export(os.path.join(output_directory, f"{title}_combined.wav"), format="wav")

def remove_local_files(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)
        print(f"Removed directory: {directory_path}")
    else:
        print(f"Directory {directory_path} does not exist.")

def generate_presigned_url(bucket_name, object_name, expiration=3600):
    """Generate a presigned URL to share an S3 object"""
    s3_client = boto3.client('s3', region_name='us-west-2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except NoCredentialsError:
        print("Credentials not available")
        return None
    return response



if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8137
    app.run(host='0.0.0.0', port=port)










"""
### This can be deleted
@app.route('/' + APP5_TITLE.lower() + '/create-audio-file', methods=['POST'])
def api_create_audio_file():
    data = {}
    try:
        data = request.get_json() # get the JSON object from the request
        #print(data)
        
    except Exception as e:
        print(e)
        return {"success": False}, 500 

    title = data["title"]

    try:
        # call your Python function to create the audio file
        print("\n\n---------GENERATING JSON---------\n\n")
        print("\n\n---------GENERATING JSON---------\n\n")
        print("\n\n---------GENERATING JSON---------\n\n")
        
        # Make sure jsondata is serializable
        try:
            jsondata = kriya_json_builder.kriya_webformat_to_json(data)
            url = r"http://192.168.0.34:5001/bambi-tts-api"
            headers = {'Content-Type': 'application/json'}
            
            # Send the request to create the tts-audio
            response = requests.post(url, json=jsondata)
            print('Response:', response.text)
            
        except (ValueError, TypeError) as e:
            print("Error: Data is not valid JSON - ", e)
            return

    
        # Print the response
        print("\nJSON Response from Remote: " + str(response.text))
        print("\nJSON Response from Remote: " + str(response.json()))
        
        print("\n\n---------JSON COMPLETE---------\\n\n")
        print("\n\n---------JSON COMPLETE---------\\n\n")
        print("\n\n---------JSON COMPLETE---------\\n\n")

        return f"audios\{title}"
    except Exception as e:
        print(e)
        return {"success": False}, 500
    
"""
"""
"""
    



"""

#sys.path.insert(1, r'\\SERVER\python server\Crystal_TTS')
sys.path.insert(1, r'\\SERVER\d\audios')
sys.path.insert(1, r'\\THE-DOCTOR\website')
sys.path.insert(1, r'\\THE-DOCTOR\website\tools')

"""







@app.route("/" + APP6_TITLE.lower())
def app6():    
    context = {
            'app_title': APP6_TITLE + ' ' + APP6_DESCRIPTION,
            'app_header': APP6_TITLE + ' ' + APP6_DESCRIPTION,
            'form_action': '/submit_' + APP6_TITLE,
            'form_label': 'Enter text for ' + APP6_TITLE
        }
    return render_template(APP6_TITLE.lower() + ".php", context=context)



@app.route('/' + APP6_TITLE.lower() + '/add_binaural_to_audio_file', methods=['POST'])
def add_binaural_to_audio_file():
    # Initialize clients for  and S3
    s3 = boto3.client('s3', region_name='us-west-2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    bucket_name = 'crystal-audio-processing'
    s3_input_file_key = 'audio-dumps/audio-combined/'
    s3_output_file_key = '' # Changes based off of preset

    try:
        print("Success!!!")
        title = request.form.get('title')
        print(title)
        preset = request.form.get('preset')  # Get preset from form data
        print(preset)
        s3_output_file_key = 'audios-draft-v1/' + preset + '/'


      ###

        # Save the audio folder locally
        audio_file_path = '/tmp/' + s3_input_file_key + title
        audio_file_output_path = '/tmp/' + s3_output_file_key + title
        
        dir_path = os.path.dirname(audio_file_path)
        dir_path_output = os.path.dirname(audio_file_output_path)

        # Check if the input directory exists and create it if necessary
        print(f"Checking directory: {dir_path}")
        if not os.path.isdir(dir_path):
            print(f"Directory '{dir_path}' not found. Creating it now...")
            os.makedirs(dir_path)
        else:
            print(f"Directory '{dir_path}' already exists.")
        
        # Check if the output directory exists and create it if necessary
        print(f"Checking directory: {dir_path_output}")
        if not os.path.isdir(dir_path_output):
            print(f"Directory '{dir_path_output}' not found. Creating it now...")
            os.makedirs(dir_path_output)
        else:
            print(f"Directory '{dir_path_output}' already exists.")
        

        print("audio file path: " + audio_file_path)
        print("audio file path: " + dir_path_output)


        print("\n\n---------Time to download the audio from S3 ---------\n\n")
        BUCKET_NAME = bucket_name
        TITLE = title
        print('we will now download the audio files following the title: ' + TITLE)
        download_files_from_s3(BUCKET_NAME, s3_input_file_key, TITLE, download_dir=audio_file_path, default_prefix=TITLE)
        files = [f for f in os.listdir(audio_file_path) if os.path.isfile(os.path.join(audio_file_path, f))]
        print(files)


###
        
        print("\n\n---------GENERATING Bineural---------\n\n")

        # Obtain the duration of the combined wav file.
        audio_file_path_filename = audio_file_path + '/' + TITLE + '_combined.wav'
        audio_length = get_audio_length(audio_file_path + '/' + TITLE + '_combined.wav')
        print(f"Duration = {audio_length}")

        # Construct the path for the output binaural file.
        bn = preset
        bineural_file_path = audio_file_output_path
        bineural_file_title = f'/{title}_ONLY_{bn}.wav'
        bineural_file_path_and_title = audio_file_output_path + f'/{title}_ONLY_{bn}.wav'
        # Create binaural audio using the preset and the duration of the input audio.
        print("\n\n---------Creating Binaural function bineural.create_binaural_audio()---------\n\n")
        output_path = bineural.create_binaural_audio(preset, audio_length, bineural_file_path, bineural_file_title, None, volume=0.1)
        print("\n\n---------Bineural Created---------\n\n")

        # Provide feedback on which audio files are being merged.
        print("\n\n---------Merging Audio with Bineural---------\n\n")
        print(f"\n\n---------Merging {audio_file_path_filename}---------")
        print(f"---------With {bineural_file_path_and_title}---------\n\n")
    
        # Construct the path for the output merged audio file.
        outTitle = f'/{title}_{bn}_draft-v1.wav'
        outfile = audio_file_output_path + outTitle

        print(f"---------Merging into: {outfile}---------\n\n")
            
        # Merge the original audio with the binaural audio.
        bineural.merge_audio_files(input_file1=audio_file_path_filename, input_file2=bineural_file_path_and_title, output_file=outfile)
        print(f"---------Saved local {outfile}---------\n\n")

        # Upload the merged audio to S3.
        print(f"---------Saving new file to S3---------\n\n")
        s3_key_combined = s3_output_file_key + outTitle
        upload_to_s3(bucket_name, s3_key_combined, outfile)

        # Remove the local temporary files.
        print(f"---------Removing local tmp files---------\n\n")
        remove_local_files(audio_file_path)

        # Generate a presigned S3 URL and send it as a success response.
        full_s3_url = generate_presigned_url(bucket_name, s3_key_combined)
        return jsonify({"status": "success", "message": full_s3_url}), 200

        
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500 



@app.route("/" + APP51_TITLE.lower())
def app51():    
    context = {
            'app_title': APP51_TITLE + ' ' + APP51_DESCRIPTION,
            'app_header': APP51_TITLE + ' ' + APP51_DESCRIPTION,
            'form_action': '/submit_' + APP51_TITLE,
            'form_label': 'Enter text for ' + APP51_TITLE
        }
    return render_template(APP51_TITLE.lower() + ".php", context=context)



@app.route('/' + APP51_TITLE.lower() + '/merge_s3_genfiles', methods=['POST'])
def merge_s3_genfiles():

    

    # Initialize clients for  and S3
    s3 = boto3.client('s3', region_name='us-west-2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    bucket_name = 'crystal-audio-processing'
    s3_gen_file_key = 'audio-dumps/audio-gen-files/'
    s3_gen_file_output_key = 'audio-dumps/audio-combined/'
    

    try:
        print("Success!!!")
        title = request.form.get('title')
        print(title)
       

        # Save the audio folder locally
        audio_file_path = '/tmp/audio-dumps/audio-gen-files/' + title
        
        dir_path = os.path.dirname(audio_file_path)
        #audio_file_path = os.path.join("audio_dump", audio_file.filename)
        
        # Check if the directory exists and create it if necessary
        print(f"Checking directory: {dir_path}")
        if not os.path.isdir(dir_path):
            print(f"Directory '{dir_path}' not found. Creating it now...")
            os.makedirs(dir_path)
        else:
            print(f"Directory '{dir_path}' already exists.")

        

        print("audio file path: " + audio_file_path)


        print("\n\n---------Time to download the audio from S3 ---------\n\n")
        BUCKET_NAME = bucket_name
        TITLE = title
        print('we will now download the audio files following the title: ' + TITLE)
        download_files_from_s3(BUCKET_NAME, s3_gen_file_key, TITLE, download_dir=audio_file_path)
        files = [f for f in os.listdir(audio_file_path) if os.path.isfile(os.path.join(audio_file_path, f))]

        # Check if audio files are mono and convert them to stereo
        for file in files:
            convert_mono_to_stereo(os.path.join(audio_file_path, file))



        print(files)


        print(f"\n\n---------Merging files within {audio_file_path}---------")
        audio_file_path_output = 'website/tools/audio_dump/' + TITLE + '/combined/'
        # Check if the directory exists and create it if necessary
        if not os.path.isdir(audio_file_path_output):
            os.makedirs(audio_file_path_output)

        merge_audio_files(audio_file_path, TITLE, audio_file_path_output)
        
        print(f"---------Merging file complete---------\n\n")

        print(f"---------Saving new file to S3---------\n\n")

        s3_key_combined = s3_gen_file_output_key + TITLE + "_combined.wav"
        upload_to_s3(bucket_name, s3_key_combined, audio_file_path_output + "/" + TITLE + "_combined.wav")
        
        print(f"---------Removing local tmp files---------\n\n")
        remove_local_files(audio_file_path)


        # Send success response to AJAX
        full_s3_url = generate_presigned_url(bucket_name, s3_key_combined)
        return jsonify({"status": "success", "message": full_s3_url}), 200

        
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500 

    
def convert_mono_to_stereo(filepath): 
    sound = AudioSegment.from_file(filepath)
    if sound.channels == 1:
        stereo_sound = AudioSegment.from_mono_audiosegments(sound, sound)
        stereo_sound.export(filepath, format="wav")
        print(f"Converted file '{filepath}' from mono to stereo")






def get_audio_length(audio_file_path):
    _, file_extension = os.path.splitext(audio_file_path)
    
    # If it's an MP3, use the pydub mediainfo method.
    if file_extension.lower() == ".mp3":
        print("mp3 detected")
        info = mediainfo(audio_file_path)
        duration = float(info["duration"])
        return duration
    
    # Otherwise, assume it's a WAV and use the wave library.
    else:
        print("assuming wav")
        with contextlib.closing(wave.open(audio_file_path,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration







@app.route("/" + APP7_TITLE.lower())
def app7():    
    context = {
            'app_title': APP7_TITLE + ' ' + APP7_DESCRIPTION,
            'app_header': APP7_TITLE + ' ' + APP7_DESCRIPTION,
            'form_action': '/submit_' + APP7_TITLE,
            'form_label': 'Enter text for ' + APP7_TITLE
        }
    return render_template(APP7_TITLE.lower() + ".php", context=context)



@app.route('/' + APP7_TITLE.lower() + '/upload_to_youtube', methods=['POST'])
def upload_to_youtube():
    # Initialize clients for  and S3
    s3 = boto3.client('s3', region_name='us-west-2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))
    bucket_name = 'crystal-audio-processing'
    
    s3_input_file_key_youtube_image = 'images/'
    
    s3_output_file_key = '' # Changes based off of preset

    try:
        print("Success!!!")
        title = request.form.get('title')
        print(title)
        preset = request.form.get('preset')  # Get preset from form data
        print(preset)
        s3_output_file_key = 'audios-youtube-mp4-v1/'
        s3_input_file_key = 'audio-draft-v1/' + preset + '/'

      ###

        # Save the audio folder locally
        audio_file_path = '/tmp/' + s3_input_file_key + title
        audio_file_output_path = '/tmp/' + s3_output_file_key + title
        youtubeImageTitle = "CrystalAI.png"
        youtube_image_path_filename = '/tmp/' + youtubeImageTitle
        dir_path = os.path.dirname(audio_file_path)
        dir_path_output = os.path.dirname(audio_file_output_path)


        # Check if the input directory exists and create it if necessary
        print(f"Checking directory: {dir_path}")
        if not os.path.isdir(dir_path):
            print(f"Directory '{dir_path}' not found. Creating it now...")
            os.makedirs(dir_path)
        else:
            print(f"Directory '{dir_path}' already exists.")
        
        # Check if the output directory exists and create it if necessary
        print(f"Checking directory: {dir_path_output}")
        if not os.path.isdir(dir_path_output):
            print(f"Directory '{dir_path_output}' not found. Creating it now...")
            os.makedirs(dir_path_output)
        else:
            print(f"Directory '{dir_path_output}' already exists.")
        

        print("audio input file path: " + audio_file_path)
        print("audio output file path: " + dir_path_output)
        print("youtube image file path: " + youtube_image_path_filename)


        print("\n\n---------Time to download the audio from S3 ---------\n\n")
        BUCKET_NAME = bucket_name
        TITLE = title
        print('we will now download the audio files following the title: ' + TITLE)
        download_files_from_s3(BUCKET_NAME, s3_input_file_key, TITLE, download_dir=audio_file_path, default_prefix=TITLE)
        files = [f for f in os.listdir(audio_file_path) if os.path.isfile(os.path.join(audio_file_path, f))]
        print(files)

        s3.download_file(BUCKET_NAME, s3_input_file_key_youtube_image + youtubeImageTitle, youtube_image_path_filename)



###
        
        print("\n\n---------Convert to mp4---------\n\n")

        # Obtain the duration of the combined wav file.
        audio_file_path_filename = audio_file_path + '/' + TITLE + '_' + preset + '_draft-v1.wav'
        audio_length = get_audio_length(audio_file_path + '/' + TITLE + '_' + preset + '_draft-v1.wav')
        print(f"Duration = {audio_length}")

        # Construct the path for the output mp4 file.
        
        mp4_file_path = audio_file_output_path
        mp4_file_title = f'/{title}.mp4'
        mp4_file_path_and_title = audio_file_output_path + f'/{title}.mp4'
        # Create binaural audio using the preset and the duration of the input audio.
        print("\n\n---------Creating mp4 function youtube.create_mp4_audio()---------\n\n")
        output_path = youtube.create_mp4_audio(audio_file_path_filename, mp4_file_path_and_title, youtube_image_path_filename)
        print("\n\n---------mp4 Created---------\n\n")

        # Provide feedback on which audio files are being merged.
        print("\n\n---------Converted Audio to MP4---------\n\n")
        print(f"\n\n---------Converted {audio_file_path_filename}---------")
        print(f"---------With {mp4_file_path_and_title}---------\n\n")
    
        # Construct the path for the output merged audio file.
        outTitle = f'/{title}.mp4'
        outfile = audio_file_output_path + outTitle


        # Upload the merged audio to S3.
        print(f"---------Saving new file to S3---------\n\n")
        s3_key_combined = s3_output_file_key + outTitle
        upload_to_s3(bucket_name, s3_key_combined, outfile)

        # Remove the local temporary files.
        print(f"---------Removing local tmp files---------\n\n")
        remove_local_files(audio_file_path)

        # Generate a presigned S3 URL and send it as a success response.
        full_s3_url = generate_presigned_url(bucket_name, s3_key_combined)
        return jsonify({"status": "success", "message": full_s3_url}), 200

        
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500 








"""
#############################################



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)

application = app

"""

"""previous


@app.route('/convert_text_to_speech', methods=['POST'])
def convert_text_to_speech():

    # Initialize clients for Polly and S3
    polly = boto3.client('polly', region_name='us-west-2')
    s3 = boto3.client('s3', region_name='us-west-2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

    bucket_name = 'crystal-audio-processing'
    s3_key = 'audio-dumps/audio-gen-files/hello_world.wav'

    # Getting text from JSON received
    data = request.get_json()
    text = data['text']

    # Use Amazon Polly to convert the text to speech
    response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')

    # If we have an audiostream in the response
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            output = os.path.join("/tmp", s3_key)
            
            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())
                
            except IOError as ioe:
                print(ioe)
                print('Error: File {} could not be written.'.format(output))
            
            else:
                # upload the file to s3
                s3.upload_file(output, bucket_name, s3_key)
                print(f'File {output} uploaded to {bucket_name} at {s3_key}')
    
    return jsonify({'message': 'Success'})

@app.route('/create_hello_world_audio')
def create_hello_world_audio():
    # Initialize clients for Polly and S3
    polly = boto3.client('polly', region_name='us-west-2')
    s3 = boto3.client('s3', region_name='us-west-2', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'), aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

    bucket_name = 'crystal-audio-processing'
    s3_key = 'audio-dumps/audio-gen-files/hello_world.wav'

    # Set text to 'Hello, world!'
    text = "Hello, world!"

    # Use Amazon Polly to convert the text to speech
    response = polly.synthesize_speech(Text=text, OutputFormat='mp3', VoiceId='Joanna')

    # If we have an audiostream in the response
    if "AudioStream" in response:
        with closing(response["AudioStream"]) as stream:
            dir_path = "/tmp/audio-dumps/audio-gen-files"

            # Check if the directories exist, and create them if they do not
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)

            output = os.path.join(dir_path, 'hello_world.wav')

            try:
                # Open a file for writing the output as a binary stream
                with open(output, "wb") as file:
                    file.write(stream.read())

            except IOError as ioe:
                print(ioe)
                print('Error: File {} could not be written.'.format(output))

            else:
                # upload the file to s3
                s3.upload_file(output, bucket_name, s3_key)
                print(f'File {output} uploaded to {bucket_name} at {s3_key}')
    
    return jsonify({'message': 'Success'})

"""