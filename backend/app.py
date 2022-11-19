import json
import time
from flask import Flask, jsonify
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
def echo(ws):
    cur = get_current()
    ws.send(json.dumps(cur, indent = 4))
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
            time.sleep(.1)
        else:
            time.sleep(5)
            

all_predictions = []
curr_song_pred = []
A = []
B = []
C = []
D = []
#Minimum threshold of eye aspect ratio below which alarm is triggerd
EYE_ASPECT_RATIO_THRESHOLD = 0.30

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


def producer(queue, event,reset):
    """Pretend we're getting a number from the network."""
    while not event.is_set() or queue.empty():
        # while True:

        cap = cv2.VideoCapture(0)
        time.sleep(0.5)
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # cv2.imshow('frame', rgb)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        # if i == 60:
        out = cv2.imwrite('capture.jpg', frame)
        # break
            # i+=1

        cap.release()
    # cv2.destroyAllWindows()



        # message = random.randint(1, 101)
        message = ['capture.jpg', rgb, gray,frame]
        # logging.info("Producer got message: %s", message)
        queue.put(message)

    # logging.info("Producer received event. Exiting")

def consumer(queue, event,reset):
    global all_predictions
    global A,B,C,D
    global curr_song_pred 
    if reset:
        curr_song_pred = []

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
            print(analyze['dominant_emotion'])
        except Exception as e: 
            print(e)
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
        if(eyeAspectRatio < EYE_ASPECT_RATIO_THRESHOLD):
            print("sleepy")
            retr.append(1)
        else:
            print("not sleep")
            retr.append(-1)
        all_predictions.append(retr)
        curr_song_pred.append(retr)
        
        # for pred in all_predictions:
            
        happy, sleepy = retr
        print(happy,sleepy)
        if happy == 1 and sleepy == -1: 
            A.append(retr)
        
        if happy == 1 and sleepy == 1: 
            B.append(retr)

        if happy == -1 and sleepy == -1: 
            C.append(retr)
        
        if happy ==- -1 and sleepy == 1: 
            D.append(retr)
        print(len(B), len(D))
       
        ret_val =[len(A)/len(all_predictions), len(B)/len(all_predictions), len(C)/len(all_predictions), len(D)/len(all_predictions)]
        print(ret_val)
        queue.clear()
    

# def calculate(queue, event):
#     global all_predictions
    
#     while not event.is_set() or not queue.empty():
#         print(len(all_predictions))
#         for pred in all_predictions:
#             if happy != 0:
#                 happy, sleepy = pred
#                 if happy == 1 and sleepy == -1: 
#                     A.append(pred)
                
#                 if happy == 1 and sleepy == 1: 
#                     B.append(pred)

#                 if happy == -1 and sleepy == -1: 
#                     C.append(pred)
                
#                 if happy ==- -1 and sleepy == 1: 
#                     D.append(pred)
#         ret_val =[len(A)/len(all_predictions), len(B)/len(all_predictions), len(C)/len(all_predictions), len(D)/len(all_predictions)]
#         print(ret_val)
#     return(ret_val)



if __name__ == "__main__":
    pipeline = queue.Queue(maxsize=1)
    event = threading.Event()
    reset = False
    while True:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            executor.submit(producer, pipeline, event, reset)
            executor.submit(consumer, pipeline, event,reset)
            # executor.submit(calculate, pipeline, event)
            # time.sleep(0.1)
            event.set()
