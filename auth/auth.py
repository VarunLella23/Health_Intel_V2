import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
from google.auth.transport.requests import Request

CLIENT_SECRETS_FILE = "googlefit.json"

# Define all necessary scopes
SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',    # Write fitness activity data
    'https://www.googleapis.com/auth/fitness.body.read',   # Write body metrics data
    'https://www.googleapis.com/auth/fitness.location.read'  # Read fitness location data
]

def authenticate_google_fit():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'googlefit.json', SCOPES, redirect_uri = 'http://localhost:8081/')
            creds = flow.run_local_server(
                port=8081,
                success_message='''
                    Authentication successful! Redirecting to dashboard...
                    <script>
                        window.location.href = "http://localhost:5000/dashboard";
                    </script>'''
            )

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build the Google Fit service
    # service = build('fitness', 'v1', credentials=creds)
    # return service