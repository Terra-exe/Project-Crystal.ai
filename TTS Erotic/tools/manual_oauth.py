from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os

# The scope for the OAuth2 request.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def main():
    # Run the OAuth flow.
    flow = InstalledAppFlow.from_client_secrets_file("tools\client_secrets.json", SCOPES)
    creds = flow.run_local_server(port=0)

    # Save the credentials to token.json.
    with open(r"tools\token.json", 'w') as token:
        token.write(creds.to_json())

if __name__ == '__main__':
    main()


