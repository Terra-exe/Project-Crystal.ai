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
from contextlib import closing
from io import BytesIO
from pydub import AudioSegment




#from flask import Flask
from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
import json_builder.bin.kriya_json_builder as kriya_json_builder
import json_builder.bin.kriya_object as kriya_object
import tools.bineural as bineural


##################
###MAIN GLOBALS###
##################

HOME_TITLE = r"Home"
APP5_TITLE = r"App5"
APP6_TITLE = r"App6"


APP5_DESCRIPTION = r"API Audio gen"
APP6_DESCRIPTION = r"Audio / Bineural Merge"


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
    s3_key = 'audio-dumps/audio-gen-files/Kriya.mp3'
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

                            segment_filename = f"genfile_{filename}_{i}_#_{value_cut}.mp3"
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
                        segment_filename_s3 = f"genfile_{filename}_{i}_#_{silent_name}.mp3"
                        segment_filename_local = generate_silent_file(int(float(value['value']) * 1000), "/tmp/silence.mp3")
                        upload_to_s3(bucket_name, s3_gen_file_key + segment_filename_s3, segment_filename_local)
                        i+=1
            
            if hasattr(e_array, 'wait'):
                for wait in e_array.wait:
                    silent_name = 'pause'
                    segment_filename_s3 = f"genfile_{filename}_{i}_#_{silent_name}.mp3"
                    segment_filename_local = generate_silent_file(int(float(wait.value) * 1000), "/tmp/silence.mp3")
                    upload_to_s3(bucket_name, s3_gen_file_key + segment_filename_s3, segment_filename_local)
                    i+=1
                        


    # Use Amazon Polly to convert the text to speech
    try:
        response = polly.synthesize_speech(Text=kriya_obj.title, OutputFormat='mp3', VoiceId='Salli')
        
    except Exception as e3:
        with open(error_file_path, 'w') as error_file:
            error_file.write(str(e3))
        s3.upload_file(error_file_path, bucket_name, s3_key_error)
        print(f"Error during conversion to speech: {e3}")
        return jsonify({'message': f'Error during conversion to speech: {e3}'}), 500

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
    silence.export(filename, format="mp3")
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
                    OutputFormat='mp3',
                    Text=text
                )
    # The response's 'AudioStream' body contains the audio data in the specified format
    audio_data = response['AudioStream'].read()

    # Save directly to an object in an S3 bucket
    write_to_s3(bucket_name, s3_key, audio_data)
                    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 8137
    app.run(host='0.0.0.0', port=port)










"""

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
#from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
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
    try:
        print("Success!!!")
        title = request.form.get('title')
        print(title)
        preset = request.form.get('preset')  # Get preset from form data
        print(preset)

        if 'audio_file' not in request.files:
            return 'No audio file uploaded.', 400
        
        audio_file = request.files['audio_file']  # Assuming file is sent under this name

        if audio_file.filename == '':
            return 'No audio file selected.', 400

        print(audio_file.filename)
        print("\n\n---------GENERATING Bineural---------\n\n")

        # Save the audio file locally
        audio_file_path = 'website/tools/audio_dump/' + audio_file.filename
        
        dir_path = os.path.dirname(audio_file_path)
        #audio_file_path = os.path.join("audio_dump", audio_file.filename)
        
        # Check if the directory exists and create it if necessary
        if not os.path.isdir(dir_path):
            os.makedirs(dir_path)

        audio_file.save(audio_file_path)

        print(audio_file_path)


        print("\n\n---------GENERATING Bineural---------\n\n")
        # Process the audio file
        audio_length = get_audio_length(audio_file_path)
        print(f"Duration = {audio_length}")
        #bineural_file_path = r'X:/website/complete audio'

        bn = "bn"
        bineural_file_path = r'X:\website\tools\audio_dump' + f'\{title}_{bn}.wav'
    
        output_path = bineural.create_binaural_audio(preset, audio_length, bineural_file_path, None, volume=0.1)
        
        print("\n\n---------Bineural Created---------\n\n")

        print("\n\n---------Merging Audio with Bineural---------\n\n")
        print(f"\n\n---------Merging {audio_file_path}---------")
        print(f"---------With {bineural_file_path}---------\n\n")
        
        #bineural.merge_audio_files(input_file1=bineural_file_path, input_file2=output_path, f"{output_path}\{title}.wav):
        outfile = r'X:\website\tools\audio_dump' + f'\{title}_bineural_complete.wav'
        bineural.merge_audio_files(input_file1=audio_file_path, input_file2=bineural_file_path, output_file=outfile)
        


        # Send success response to AJAX
        return jsonify({"status": "success", "message": f"audios\{title}"}), 200
        
    except Exception as e:
        print(e)
        return jsonify({"status": "error", "message": str(e)}), 500 

def get_audio_length(audio_file_path):
    with contextlib.closing(wave.open(audio_file_path,'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
        return duration

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