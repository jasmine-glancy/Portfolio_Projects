import requests
from dotenv import load_dotenv
import os

load_dotenv('secrets.env')

JG_SPOTIFY_CLIENT_ID= os.getenv('JG_SPOTIFY_CLIENT_ID')

JG_CLIENT_SECRET = os.getenv('JG_CLIENT_SECRET')

JG_SPOTIFY_ENDPOINT = "https://accounts.spotify.com/authorize" 

def Jg_Authenticate_Spotify():
    """Authenticate your Python project with Spotify using your unique Client ID/ Client Secret."""

    jg_spotify_params = {
        "client_id": JG_SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "http://localhost:4304/auth/spotify/callback", 
        "scope": "playlist-modify-public playlist-modify-private"
    }


    # Authenticate your Python project with Spotify using your unique Client ID/ Client Secret.
    jg_spotify_response = requests.get(url=JG_SPOTIFY_ENDPOINT, params=jg_spotify_params)
    print(jg_spotify_response.text)

Jg_Authenticate_Spotify()