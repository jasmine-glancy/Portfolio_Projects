"""Welcome to the musical time machine!"""
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_auth import JG_SPOTIFY_CLIENT_ID, JG_CLIENT_SECRET
from pprint import pprint


load_dotenv('secrets.env')

jg_spotify_user_id = os.getenv('jg_spotify_user_id')
jg_spotify_token = os.getenv('jg_spotify_token')

# Asks user what year they would like to time travel to

jg_music_date = input("What year would you like to travel to? (YYYY-MM-DD): ")

jg_billboard_response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{jg_music_date}")
jg_soup = BeautifulSoup(jg_billboard_response.text, "html.parser")

# Select the songs from the webpage
jg_songs = jg_soup.select(selector="li h3")

# Create a list of spotify song URIs for the list of song names from the top 100
jg_song_titles_list = [jg_song.getText().replace("\n", "").replace("\t","").replace('"', "'").split("ft.")[0] for jg_song in jg_songs]
jg_song_titles = jg_song_titles_list[:-9]
print(jg_song_titles)
    
# Get artist information
jg_artists = jg_soup.select(selector="li span", class_="c-label a-no-truncate")
jg_artist_data = [jg_artist.getText().replace("\n", "").replace("\t","") for jg_artist in jg_artists]

# Gets the first and last artist from the list
jg_artist_list = jg_artist_data[16:-34]


# Gets artist names and puts them in a list
jg_artist_names = [jg_artist.replace(" X ", ", ").replace("&", ",").replace("Featuring", ",").replace(" ,", ",").replace(":", ",") for jg_artist in jg_artist_list if not jg_artist.isdigit() and jg_artist != "-" and jg_artist != "NEW" and jg_artist != "RE" and jg_artist != "RE-ENTRY"]

print(jg_artist_names)
# authenticate your Python project with Spotify using your unique Client ID/ Client Secret.
jg_sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=JG_SPOTIFY_CLIENT_ID,
                                                  client_secret=JG_CLIENT_SECRET,
                                                  redirect_uri="http://localhost:4304/auth/spotify/callback", 
                                                  scope="playlist-modify-public playlist-modify-private",
                                                  show_dialog=True,
                                                  cache_path=jg_spotify_token,
                                                  username=jg_spotify_user_id
                                                  ))

jg_user_id = jg_sp.current_user()["id"]


# Create a new private playlist with the name "YYYY-MM-DD Billboard 100"
jg_new_billboard_100 = jg_sp.user_playlist_create(user=jg_user_id, name=f"{jg_music_date} Billboard 100", public=False, collaborative=False, description=f"The top 100 songs from {jg_music_date}! Enjoy your blast from the past.")

def add_to_playlist(jg_title, jg_artist):

    jg_search_results = jg_sp.search(f"track:{jg_title} artist:{jg_artist}",
                       type="track", limit=10)
    try:
        jg_song_uri = jg_search_results["tracks"]["items"][0]["uri"]
    except IndexError:
        print(f"{jg_title} by {jg_artist} did not return any result")
        return None
    else:
        jg_songs_uris_list = []
        jg_songs_uris_list.append(jg_song_uri)
        jg_sp.playlist_add_items(playlist_id=jg_new_billboard_100["id"], items=jg_songs_uris_list)

 
 
for jg_counter, jg_song_title in enumerate(jg_song_titles):
    jg_artist = jg_artist_names[jg_counter]
    jg_title = jg_song_title
    add_to_playlist(jg_title, jg_artist)


