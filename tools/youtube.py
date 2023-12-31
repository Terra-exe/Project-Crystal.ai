from moviepy.editor import AudioFileClip, ImageClip
import numpy as np
import wave
import struct
import os
from .audio_generator import AudioGenerator

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload




# Scopes required by YouTube API
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']





def create_mp4_audio(source_wav, save_path, youtube_image_path_filename):
    try:
        print("Source wav: ", source_wav)
        print("Save mp4 Path: ", save_path)
        # Check if audio file exists
        if not os.path.exists(source_wav):
            print("Audio source file does not exist")
            return None

        print("Save mp4 Path: ", save_path)

        # Check if path for saving exists
        save_dir = os.path.dirname(save_path)
        if not os.path.exists(save_dir):
            print("Save directory does not exist, creating.")
            os.makedirs(save_dir, exist_ok=True)
            
        
        # Load your audio file
        audio_clip = AudioFileClip(source_wav)

        # Check if image file exists
        if not os.path.exists(youtube_image_path_filename):
            print("Image file does not exist")
            return None

        # Load an image or create a color clip
        image_clip = ImageClip(youtube_image_path_filename, duration=audio_clip.duration)

        # Set the audio of the image clip as your audio file
        video_clip = image_clip.set_audio(audio_clip)

        # Write the result to a file
        video_clip.write_videofile(save_path, fps=24)

        print(f"save_path = {save_path}")

        return save_path

    except Exception as e:
        print("An error occurred: ", str(e))
        return None
    
    
'''

def create_mp4_audio(source_wav, save_path, youtube_image_path_filename):
        
    print("Source wav: ", source_wav)    
    print("Save mp4 Path: ", save_path)

    # Load your audio file
    audio_clip = AudioFileClip(source_wav)

    # Load an image or create a color clip
    image_clip = ImageClip(youtube_image_path_filename, duration=audio_clip.duration)

    # Set the audio of the image clip as your audio file
    video_clip = image_clip.set_audio(audio_clip)

    # Write the result to a file
    video_clip.write_videofile(save_path, fps=24)
   
   

    
    print(f"save_path = {save_path}")

   

    return save_path

'''

def uploadToYouTube(youtube_path_filename, title):

    print("Starting the YouTube upload process...")

    # Load credentials and create an OAuth flow
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('tools/token.json'):
        print("Credential file found, loading credentials...")
        creds = Credentials.from_authorized_user_file('tools/token.json', SCOPES)
    else:
        print("Credential file not found.")

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Credentials have expired, refreshing...")
            creds.refresh(Request())
        else:
            raise FileNotFoundError("No credentials available for YouTube API access.")
    else:
        print("Credentials are valid.")

    youtube = build('youtube', 'v3', credentials=creds)
    print("YouTube service built successfully.")

    # Prepare the video request body
    body = {
        'snippet': {
            'title': title,
            'description': 'An episode of the Bambi Cloud Podcast on self-help, feminine empowerment, and spiritual enlightenment.\nThese episodes have been generated programmatically based off as simple text submission as input, and therefore may be subject to change over time.\nDo you pray at the altar of chaos?\nModern Gods for Modern Girls.\nOur Lady of Perpetual Chaos:     x.com/Terra_Infinity    \nWelcome to the opera, dear humans.',
            'tags': ['Bambi', 'Bambi Sleep', 'Bambi Cloud', 'Bambi Enlightned', 'Spirituality', 'Meditation', 'Fantasy', 'Story', 'Roleplay', 'Podcast', 'Grimes', 'Modern Girls', 'Altar of Chaos', 'elf tech', 'spirit tech', 'spiritual tech', 'spiritual technology', 'chaos', 'chaos manual', 'media empire', 'god drop', 'Made not born', 'consciousness', 'Chaos tm', 'demi-god', 'modular spirituality', 'polytheistic spirituality', 'pantheistic spirituality', 'holy crusade', 'Miss Anthropocene', 'Cyber Athens'],
            #'tags': ['Bambi Enlightned', 'Spirituality', 'Meditation', 'Fantasy', 'Story'],
            'categoryId': '24'  # You can get the category ID from YouTube's API
            # Educational (27) - If the content explores teaching, wisdom, consciousness, meditation techniques, this category could be a good match.
            # Howto & Style (26) - If the content is instructional, particularly regarding self-help, meditation, and spiritual practices, consider this category.
            # Entertainment (24) - Use if the content employs fantasy role play, and more generally seeks to entertain the viewer.
            # Science & Technology (28) - Use if the content is deeply analytical, and uses scientific research in a meaningful way.
        },
        'status': {
            'privacyStatus': 'private',  # You can set to public, private, or unlisted
        }
    }

    print(f"Body for the video request prepared: {body}")

    # Call the YouTube API to upload the file
    print("Calling the YouTube API to upload the file...")
    request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(youtube_path_filename, chunksize=-1, resumable=True)
    )


    response = None
    while response is None:
        try:
            print("Uploading the video...")
            status, response = request.next_chunk()
            if status:
                print("Uploaded %d%%." % int(status.progress() * 100))
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    
    if response is not None:
        print("Upload Complete!")
        print(f"Video ID: {response.get('id')}")
    else:
        print("Upload failed.")       

