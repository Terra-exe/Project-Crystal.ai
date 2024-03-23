import requests

url = "https://api.elevenlabs.io/v1/text-to-speech/jsCqWAovK2LkecY7zXl4/stream"

querystring = {"output_format":"mp3_22050_32"}

payload = {
    "voice_settings": {
        "similarity_boost": 1,
        "stability": 1
    },
    "text": "test"
}
headers = {
    "xi-api-key": "a1fd630e18d08e2e26bd309d4c35143e",
    "Content-Type": "application/json"
}

response = requests.request("POST", url, json=payload, headers=headers, params=querystring)

print(response.text)