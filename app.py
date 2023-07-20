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
#sys.path.insert(1, r'\\SERVER\python server\Crystal_TTS')
sys.path.insert(1, r'\\SERVER\d\audios')
sys.path.insert(1, r'\\THE-DOCTOR\website')
sys.path.insert(1, r'\\THE-DOCTOR\website\tools')

#sys.path.append(r"C:\python server\Crystal_TTS")


#sys.path.append(r"D:\audios")
import io

from flask import Flask, request, jsonify, render_template, send_file, send_from_directory
from ifttt_webhook import webhook, run_app_script
import TTS.crystal_tts as crystalTTS
import json_builder.bin.kriya_json_builder as kriya_json_builder
import tools.bineural as bineural

#disabled because the server can't handle.
#import app_tools.transcription.bin.transcribe_audio as transcribe_audio
#import ai_models.SummarizeAI.bin.summaryai as summary_ai


##################
###MAIN GLOBALS###
##################

HOME_TITLE = r"Home"
APP5_TITLE = r"App5"
APP6_TITLE = r"App6"


APP5_DESCRIPTION = r"API Audio gen"
APP6_DESCRIPTION = r"Audio / Bineural Merge"



###########
###FLASK###
###########

app = Flask(__name__)
app.register_blueprint(webhook, url_prefix='/')

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
    return send_file(r'\\THE-DOCTOR\website\TTS\audios\demos\crystal_demo.wav', mimetype='audio/wav')

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


#############################################



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)