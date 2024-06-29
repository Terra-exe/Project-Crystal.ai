



import os
import subprocess
import spotipy
import shutil
from spotipy.oauth2 import SpotifyClientCredentials

# Function to download a Spotify playlist to MP3
def download_spotify_playlist(playlist_url, download_directory='D:\\tmp\\glaum mp3s'):
    # Set environment variables for Spotify API credentials
    os.environ['SPOTIPY_CLIENT_ID'] = '142454a850f140ddb6b06eb6492b7514'
    os.environ['SPOTIPY_CLIENT_SECRET'] = '0d6e6cbc084345309bb836d478143b10'
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'
    # Initialize Spotify API client
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())

    # Extract playlist ID from URL
    playlist_id = playlist_url.split('/')[-1].split('?')[0]

    # Get playlist tracks
    playlist_tracks = sp.playlist_tracks(playlist_id)['items']

    # Create a directory to save the MP3 files
    os.makedirs(download_directory, exist_ok=True)

    # Iterate through each track in the playlist
    for item in playlist_tracks:
        track = item['track']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        search_query = f"{artist_name} - {track_name}"

        # Construct the command to use the spotdl CLI
        output_path = os.path.join(download_directory, f'{artist_name} - {track_name}.mp3')
        command = [
            'spotdl', search_query,
            '--output', output_path
        ]
        
        # Run the command and check the result
        result = subprocess.run(command, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Downloaded: {artist_name} - {track_name}")
        else:
            print(f"Error downloading {artist_name} - {track_name}:")
            print(result.stderr)

    # Move all downloaded MP3 files to the final directory
    final_directory = os.path.join(download_directory, 'extra glaum mantras')
    os.makedirs(final_directory, exist_ok=True)

    for root, dirs, files in os.walk(download_directory):
        for file in files:
            if file.endswith('.mp3'):
                file_path = os.path.join(root, file)
                destination_path = os.path.join(final_directory, file)
                if os.path.exists(destination_path):
                    base, extension = os.path.splitext(destination_path)
                    counter = 1
                    new_destination_path = f"{base}_{counter}{extension}"
                    while os.path.exists(new_destination_path):
                        counter += 1
                        new_destination_path = f"{base}_{counter}{extension}"
                    destination_path = new_destination_path
                shutil.move(file_path, destination_path)
                print(f"Moved: {file}")
# Replace with your Spotify playlist URL

#casey
playlist_url = 'https://open.spotify.com/playlist/17yXaAwDtRZJdj6h0mZZzx?si=d8ca1e8790cf4c2e'

#glaum2024
# playlist_url = 'https://open.spotify.com/playlist/5JiZXhOKIpSxUn3fAeH55P?si=8a43c8e082434387'

#glaum extra

#playlist_url = 'https://open.spotify.com/playlist/3gvnAB4nEuNYptQyIShJfK?si=bf0fc2a2aeb149c5'


# Call the function to download the playlist
download_spotify_playlist(playlist_url)