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
APP1_TITLE = r"App1"
APP2_TITLE = r"App2"
APP3_TITLE = r"App3"
APP4_TITLE = r"App4"
APP5_TITLE = r"App5"
APP6_TITLE = r"App6"


APP1_DESCRIPTION = r"Transcribe Youtube to Summary Audio"
APP2_DESCRIPTION = r"Upload JSON to Audio"
APP3_DESCRIPTION = r"Local audio gen"
APP4_DESCRIPTION = r"Copy of - Transcribe Youtube to Summary Audio"
APP5_DESCRIPTION = r"API Audio gen"
APP6_DESCRIPTION = r"Audio / Bineural Merge"



###########
###FLASK###
###########

app = Flask(__name__)
app.register_blueprint(webhook, url_prefix='/')

@app.route("/")
def index():
    context = {
        'app_title': HOME_TITLE + ' Inactive Page',
        'app_header': HOME_TITLE + ' Inactive Page',
        'form_action': '/submit' + HOME_TITLE,
        'form_label': 'Enter text for ' + HOME_TITLE
    }
    return render_template("index.php", context=context)

@app.route("/" + APP1_TITLE.lower())
def app1():
    context = {
        'app_title': APP1_TITLE + ' ' + APP1_DESCRIPTION,
        'app_header': APP1_TITLE + ' ' + APP1_DESCRIPTION,
        'form_action': '/submit_' + APP1_TITLE,
        'form_label': 'Enter YouTube URL for ' + APP1_TITLE
    }
    return render_template("app1.php", context=context)

@app.route("/" + APP1_TITLE.lower() + "/list_summary_files")
def list_summary_files():
    path = r'\\server\python server\website\app_tools\summarization\summary_texts'
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return jsonify(files)


@app.route('/' + APP1_TITLE.lower() + '/replay-summary', methods=['POST'])
def replay_summary():
    print("---Received POST to python---")
    data = {}
    try:
        data = request.get_json() # get the JSON object from the request
        summary_filename = os.path.join(r"\\server\python server\website\app_tools\summarization\summary_texts", data["filename"])
        print("X!X!X!X!  "  +  summary_filename  + "    X!X!X!X!")
        server_ip = "server"  # Replace with the actual IP address of the server
        port = 13713  # Replace with the correct port number

        send_string_to_server(server_ip, port, summary_filename)

        
    except Exception as e:
        print(e)
        return {"success": False}, 500 
    
    return "Success"


@app.route("/" + APP2_TITLE.lower())
def app2():
    context = {
        'app_title': APP2_TITLE + ' ' + APP2_DESCRIPTION,
        'app_header': APP2_TITLE + ' ' + APP2_DESCRIPTION,
        'form_action': '/submit_' + APP2_TITLE,
        'form_label': 'Enter text for ' + APP2_TITLE
    }
    return render_template("app2.php", context=context)


@app.route("/" + APP3_TITLE.lower())
def app3():
    context = {
        'app_title': APP3_TITLE + ' ' + APP3_DESCRIPTION,
        'app_header': APP3_TITLE + ' ' + APP3_DESCRIPTION,
        'form_action': '/submit_' + APP3_TITLE,
        'form_label': 'Enter text for ' + APP3_TITLE
    }
    return render_template(APP3_TITLE.lower() + ".php", context=context)

@app.route("/" + APP3_TITLE.lower() + "/audio/crystal_demo")
def serve_audio():
    return send_file(r'\\server\python server\website\TTS\audios\demos\crystal_demo.wav', mimetype='audio/wav')

@app.route('/' + APP3_TITLE.lower() + '/create-audio-file', methods=['POST'])
def create_audio_file():
    data = {}
    try:
        data = request.get_json() # get the JSON object from the request
        print(data)
        
    except Exception as e:
        print(e)
        return {"success": False}, 500 

    title = data["title"]

    try:
        # call your Python function to create the audio file
        #audio_file_path = crystalTTS.create_audio_file_single_phrase(title, data)
        print("\n\nJSON OUTPUT\n\n")
        jsondata = kriya_json_builder.kriya_webformat_to_json(data)
        audio_file_path = crystalTTS.json_to_audio(jsondata)
        #print(jsondata)
        print("\n\nJSON COMPLETE\n\n")
        return f"audios\{title}"
    except Exception as e:
        print(e)
        return {"success": False}, 500



@app.route('/audios/<path:filename>', endpoint='audio_endpoint')
def serve_audio(filename):
    return send_from_directory('D:\\audios', filename + '_combined.wav', as_attachment=True)

@app.route("/" + APP4_TITLE.lower())
def app4():
    context = {
            'app_title': APP4_TITLE + ' ' + APP4_DESCRIPTION,
            'app_header': APP4_TITLE + ' ' + APP4_DESCRIPTION,
            'form_action': '/submit_' + APP4_TITLE,
            'form_label': 'Enter text for ' + APP4_TITLE
        }
    return render_template(APP4_TITLE.lower() + ".php", context=context)

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