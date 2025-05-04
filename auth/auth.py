import os
import secrets
from flask import Flask, redirect, request, session, url_for
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from functools import wraps
import pickle

# Configure Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", secrets.token_hex(16))

# OAuth Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI")

# Google Fit Scopes
SCOPES = [
    'https://www.googleapis.com/auth/fitness.activity.read',
    'https://www.googleapis.com/auth/fitness.body.read',
    'https://www.googleapis.com/auth/fitness.location.read'
]

# Client configuration from environment variables
CLIENT_CONFIG = {
    "web": {
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": [REDIRECT_URI]
    }
}

def authenticate_google_fit():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'credentials' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login')
def login():
    # Create flow instance using client config
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_config(
        CLIENT_CONFIG,
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )
    
    flow.fetch_token(authorization_response=request.url)
    
    credentials = flow.credentials
    session['credentials'] = credentials_to_dict(credentials)
    
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
@login_required
def dashboard():
    credentials = Credentials(**session['credentials'])
    
    if credentials.expired:
        credentials.refresh(Request())
        session['credentials'] = credentials_to_dict(credentials)
    
    # Add Google Fit API calls here
    return "Dashboard - Authenticated Successfully!"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/')
def index():
    return '<a class="button" href="/login">Authenticate with Google</a>'

def run_local_server():
    app.run(host='localhost', port=5000, ssl_context='adhoc')

if __name__ == '__main__':
    if os.environ.get('FLASK_ENV') == 'production':
        app.run()
    else:
        run_local_server()