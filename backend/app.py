import json
import time
from flask import Flask, jsonify, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import cred
from flask_cors import CORS
from flask_sock import Sock
import concurrent.futures
import queue
import threading
import time
from tkinter.messagebox import RETRY
import cv2
from deepface import DeepFace
import numpy as np  #this will be used later in the process
import time
from threading import Thread

#Import necessary libraries
from scipy.spatial import distance
from imutils import face_utils
import numpy as np
import time
import dlib
import cv2
from bpmsort import mood_changer

scope = "user-read-recently-played user-read-currently-playing ugc-image-upload user-read-private user-library-modify playlist-modify-public user-library-read playlist-read-private playlist-read-collaborative app-remote-control streaming"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=cred.client_id, client_secret= cred.client_secret, redirect_uri=cred.redirect_url, scope=scope))
app = Flask(__name__)
CORS(app)

sock = Sock(app)

USER_ID = sp.me()['id']

happy_prod = 0 #playlists
happy_unprod = 0 
sad_prod = 0
sad_unprod = 0
prevPlayed = []
predicted_mood = 0
all_predictions = []
curr_song_pred = [0,0,0,0]
proportions =[]
retr = []
A = []
B = []
C = []
D = []
reset = False
song_history = {}
random_second_next = None
first_iter = True

@app.route("/playlists")
def get_playlists():
    return sp.current_user_playlists()

@app.route("/previoussongs")
def previous_songs():
    return sp.current_user_recently_played(limit=12)

@app.route("/current")
def get_current():
    global next_song_id
    global reset
    global predicted_mood
    global curr_song_pred 
    global first_iter
    global random_second_next
    global song_history
    playing = sp.current_user_playing_track()
    if playing:
        # print(playing['item']['id'])
        curr_song_id = playing['item']['id']
        if(playing['item']['duration_ms'] - playing['progress_ms'] <= 20000):
            if(reset!=True):
                print("RESET",reset)
                reset = True
                if len(curr_song_pred) > 0:
                    max_value = max(curr_song_pred)
                    max_index = curr_song_pred.index(max_value)
                    predicted_mood = max_index
                    # next_song_id must be sent to the front to be displayed
                    # print("here")
                    print(curr_song_id)
                    # print(happy_prod)
                    # print(happy_unprod)
                    # print(sad_unprod)
                    # print(sad_prod)
                    # print(sad_unprod)
                    # print(max_index)
                    # print(sp)
                    print("finished here")
                    next_song_id, random_second_next, song_history = mood_changer(first_iter, random_second_next, curr_song_id, 
                    happy_prod, happy_unprod, sad_prod, sad_unprod, max_index, song_history, sp)
                    first_iter = False
                    # the random next song is only to be shown to the user.
                    # TODO: the condition of whether or not there is no song remaining must be checked

                    print(random_second_next)
                    sp.add_to_queue(next_song_id)
                    # sp.add_to_queue(random_second_next)
        else:
            reset = False
        return playing

    return jsonify("None")

@sock.route('/streamtrack')
def trackinfo(ws):
    cur = get_current()
    
    songSend = {}
    songSend['song'] = cur

    ws.send(json.dumps(songSend, indent = 4))

    global random_second_next

    sent_next = random_second_next
    while True:
        tempCur = get_current()
        if(tempCur!=cur):
            if(tempCur and tempCur["item"]["name"] != cur["item"]["name"]):
                print("RESET in getcurloop")
                global curr_song_pred
                curr_song_pred = [0,0,0,0]
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
            if(random_second_next!=None and random_second_next!=sent_next):
                sent_next = random_second_next
                songSend = {}
                songSend['upnext'] = sent_next
                print("sending next")
                uptrackinfo = sp.track(sent_next)
                print(uptrackinfo)
                ws.send(json.dumps(uptrackinfo, indent = 4))
            cur = tempCur
            songSend = {}
            songSend['song'] = tempCur
            ws.send(json.dumps(songSend, indent = 4))
            time.sleep(1)
        else:
            time.sleep(5)

def build_json(p_x, p_y):
    global curr_song_pred
    res = {}
    res['x'] = p_x
    res['y'] = p_y
    if sum(curr_song_pred) != 0:
        res['avgx'] = ((curr_song_pred[0] + curr_song_pred[2]) *1 + ((curr_song_pred[1] + curr_song_pred[3]) * -1 ))/ (sum(curr_song_pred))
        res['avgy'] = ((curr_song_pred[0] + curr_song_pred[1]) *1 + ((curr_song_pred[2] + curr_song_pred[3]) * -1 ))/ (sum(curr_song_pred))
        print(res['avgx'], res['avgy'])
    else:
        res['avgx'] = 0
        res['avgy'] = 0

    return json.dumps(res, indent=4)

@sock.route('/mlresult')
def mlinfo(ws):
    global retr
    global all_predictions
    local_x =0
    local_y =0
    y_axis = 0
    x_axis = 0
    # if len(retr) > 0:
    #     emotion = retr[0]
    #     # print(retr)

    #     x_axis= len(all_predictions)
    #     y_axis= emotion  
    #     local_x = x_axis
    #     local_y = y_axis

    ws.send(build_json(local_x, local_y))

    while True:
        if len(retr) > 1:
            # print("valid values, reseeting ")
            y_axis = retr[0]
            x_axis= retr[1]
        # if(local_y != y_axis or local_x != x_axis):
            # print("HERE")
            # print(local_x , local_y)
        # local_x = x_axis
        # local_y = y_axis
        # print(local_x , local_y)
        ws.send(build_json(-x_axis, y_axis))
        time.sleep(1.5)
        # else:
        #     # print("NO UPDATE")
        #     time.sleep(1.5)

@app.route("/predictions")
def get_prediction_average():
    global proportions 
    return proportions

@app.route("/submit-playlists", methods=["POST"])
def receive_playlists():
    global happy_prod
    global happy_unprod 
    global sad_prod 
    global sad_unprod 
    happy_prod = request.json['happy_prod']['id']
    happy_unprod = request.json['happy_unprod']['id']
    sad_prod = request.json['sad_prod']['id']
    sad_unprod = request.json['sad_unprod']['id']
    # print(happy_prod)
    # print(happy_unprod)
    # print(sad_prod)
    # print(sad_unprod)
    t1 = threading.Thread(target=p, args=())
    t1.start()
    return {}

   

def p():
    # print("im here")
    pipeline = queue.Queue(maxsize=1)
    event = threading.Event()
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(producer, pipeline, event)
            executor.submit(consumer, pipeline, event)
            # executor.submit(calculate, pipeline, event)
            # time.sleep(0.1)
            event.set()




    # return True

#Minimum threshold of eye aspect ratio below which alarm is triggerd
EYE_ASPECT_RATIO_THRESHOLD = 0.24

#Minimum consecutive frames for which eye ratio is below threshold for alarm to be triggered
EYE_ASPECT_RATIO_CONSEC_FRAMES = 10

#COunts no. of consecutuve frames below threshold value
COUNTER = 0

#Load face cascade which will be used to draw a rectangle around detected faces.
face_cascade = cv2.CascadeClassifier("haarcascades/haarcascade_frontalface_default.xml")

#This function calculates and return eye aspect ratio
def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])

    ear = (A+B) / (2*C)
    return ear

#Load face detector and predictor, uses dlib shape predictor file
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

#Extract indexes of facial landmarks for the left and right eye
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']


def producer(queue, event):
    """Pretend we're getting a number from the network."""
    while not event.is_set() or queue.empty():
        # while True:

        cap = cv2.VideoCapture(0)
        time.sleep(0.5)
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out = cv2.imwrite('capture.jpg', frame)
        cap.release()

        message = ['capture.jpg', rgb, gray,frame]

        queue.put(message)


def consumer(queue, event):
    global all_predictions
    global A,B,C,D
    global curr_song_pred 
    global proportions 
    global reset
    global retr

    if reset:
        curr_song_pred = [0,0,0,0]

    while not event.is_set() or not queue.empty():
        message = queue.get()

        imgpath, rgb, gray,frame = message
        retr = []
        """Pretend we're saving a number in the database."""
        # imgpath = 'capture.jpg' 
        image = cv2.imread(imgpath)
        try:
            analyze = DeepFace.analyze(image,actions=['emotion']) 
            if analyze['dominant_emotion'] in ['sad', 'fear', 'digust', 'scared']:
                retr.append(-1)
            elif analyze['dominant_emotion'] in ['happy', 'surprised','neutral']:
                retr.append(1)
            # retr.append() #here the first parameter is the image we want to analyze #the second one there is the action
            # print(analyze['dominant_emotion'])
        except Exception as e: 
            # print(e)
            retr.append(0)
            

        face = detector(gray, 0)
        face_rectangle = face_cascade.detectMultiScale(gray, 1.3, 5)
        shape = predictor(gray, face[0])
        shape = face_utils.shape_to_np(shape)

        #Get array of coordinates of leftEye and rightEye
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        #Calculate aspect ratio of both eyes
        leftEyeAspectRatio = eye_aspect_ratio(leftEye)
        rightEyeAspectRatio = eye_aspect_ratio(rightEye)

        eyeAspectRatio = (leftEyeAspectRatio + rightEyeAspectRatio) / 2
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        #Detect if eye aspect ratio is less than threshold

        if analyze['dominant_emotion'] == "happy":
            print("happy here")
            EYE_ASPECT_RATIO_THRESHOLD = 0.05
        else:
            EYE_ASPECT_RATIO_THRESHOLD = 0.24

        if(eyeAspectRatio < EYE_ASPECT_RATIO_THRESHOLD):
            print("sleepy")
            retr.append(1)
        else:
            print("not sleep")
            retr.append(-1)
        all_predictions.append(retr)
        # curr_song_pred.append(retr)
        
        # for pred in all_predictions:
            
        happy, sleepy = retr
        print(happy,sleepy)
        if happy == 1 and sleepy == -1: 
            A.append(retr)
            curr_song_pred[0] +=3
        
        if happy == 1 and sleepy == 1: 
            B.append(retr)
            curr_song_pred[1] +=3

        if happy == -1 and sleepy == -1: 
            C.append(retr)
            curr_song_pred[2] +=3
        
        if happy == -1 and sleepy == 1: 
            D.append(retr)
            curr_song_pred[3] +=3
        

        # print(len(B), len(D)x)
        
        proportions =[len(A)/len(all_predictions), len(B)/len(all_predictions), len(C)/len(all_predictions), len(D)/len(all_predictions)]
        print(proportions)
        queue.clear()

def start_prediction():
    pipeline = queue.Queue(maxsize=1)
    event = threading.Event()
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(producer, pipeline, event)
            executor.submit(consumer, pipeline, event)
            event.set()
