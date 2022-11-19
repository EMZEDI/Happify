import time
from flask import Flask, jsonify
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import cred
from flask_cors import CORS
from flask_sock import Sock

scope = "user-read-recently-played user-read-currently-playing ugc-image-upload user-read-private user-library-modify playlist-modify-public user-library-read playlist-read-private playlist-read-collaborative app-remote-control streaming"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret= cred.client_secret, redirect_uri=cred.redirect_url, scope=scope))
app = Flask(__name__)
CORS(app)

sock = Sock(app)

USER_ID = sp.me()['id']

@app.route("/playlists")
def get_playlists():
    return sp.current_user_playlists()

@app.route("/previoussongs")
def previous_songs():
    return sp.current_user_recently_played()

@app.route("/current")
def get_current():
    playing = sp.current_user_playing_track()
    if playing:
        return playing
    return jsonify("None")

@sock.route('/streamtrack')
def echo(ws):
    cur = get_current()
    ws.send(cur)
    while True:
        tempCur = get_current()
        if(tempCur!=cur):
            cur = tempCur
            ws.send(tempCur)
            time.sleep(1)
        else:
            time.sleep(5)