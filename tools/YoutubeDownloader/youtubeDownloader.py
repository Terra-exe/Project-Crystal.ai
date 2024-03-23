"""import yt_dlp

def download_video_as_mp3(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # Save the file in a "downloads" subfolder with the specified filename template
        'outtmpl': 'downloads/%(title)s-%(id)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    video_url = 'https://youtu.be/pHDuLJfmw1c?si=cH-D9Titm0yWgsm7'
    download_video_as_mp3(video_url)


"""


import yt_dlp

def download_playlist_as_mp3(playlist_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'tools/YoutubeDownloader/downloads/%(playlist_title)s/%(title)s-%(id)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([playlist_url])

if __name__ == "__main__":
    playlist_url = 'https://www.youtube.com/playlist?list=PLAVn_5RpZzNSx7HZ-VaY7yDRZ3oe3C6QG'
    download_playlist_as_mp3(playlist_url)



