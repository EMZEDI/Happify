import json
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

prevPlayed = []


@app.route("/playlists")
def get_playlists():
    return sp.current_user_playlists()

@app.route("/previoussongs")
def previous_songs():
    return sp.current_user_recently_played(limit=12)

@app.route("/current")
def get_current():
    playing = sp.current_user_playing_track()
    if playing:
        return playing
    return jsonify("None")

@sock.route('/streamtrack')
def trackinfo(ws):
    cur = get_current()
    
    songSend = {}
    songSend['song'] = cur

    ws.send(json.dumps(songSend, indent = 4))

    while True:
        tempCur = get_current()
        if(tempCur!=cur):
            if(tempCur and tempCur["item"]["name"] != cur["item"]["name"]):
                # print(tempCur["item"]["name"])
                prevPlayed.append(cur)
                if(len(prevPlayed) > 14):
                    prevPlayed.pop(0)
                # for item in prevPlayed:
                #     print(item["item"]["name"])
                listjson = json.dumps(prevPlayed)
                arraySend = {}
                arraySend['played'] = listjson
                ws.send(json.dumps(arraySend, indent=4))
            cur = tempCur
            songSend = {}
            songSend['song'] = tempCur
            ws.send(json.dumps(songSend, indent = 4))
            time.sleep(1)
        else:
            time.sleep(5)

def build_json(p_x, p_y):
    res = {}
    res['x'] = p_x
    res['y'] = p_y
    return json.dumps(res, indent=4)

@sock.route('/mlresult')
def mlinfo(ws):
    x_axis=0.0
    y_axis=1.0
    local_x = x_axis
    local_y = y_axis

    ws.send(build_json(local_x, local_y))

    while True:
        if(x_axis<1):
            x_axis=x_axis+.2
        else:
            x_axis=x_axis-2
        if(y_axis<1):
            y_axis=y_axis+.2
        else:
            y_axis=y_axis-2
        if(local_y != y_axis or local_x != x_axis):
            local_x = x_axis
            local_y = y_axis
            ws.send(build_json(local_x, local_y))
            time.sleep(1.5)
        else:
            time.sleep(5)