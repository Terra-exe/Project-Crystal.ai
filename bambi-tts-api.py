from flask import Flask, request, jsonify
import boto3
from contextlib import closing
import os

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run()