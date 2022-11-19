from tkinter.messagebox import RETRY
import cv2
from deepface import DeepFace
import numpy as np  #this will be used later in the process
import time

#Import necessary libraries
from scipy.spatial import distance
from imutils import face_utils
import numpy as np
import time
import dlib
import cv2

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


def detect():
    retr = []
    #Start webcam video capture
    video_capture = cv2.VideoCapture(0)

    cap = cv2.VideoCapture(0)

    i = 0
    while(True):
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', rgb)
        if cv2.waitKey(1) & 0xFF == ord('q'):
        # if i == 60:
            out = cv2.imwrite('capture.jpg', frame)
            break
        i+=1

    cap.release()
    cv2.destroyAllWindows()

    imgpath = 'capture.jpg' 
    image = cv2.imread(imgpath)
    try:
        analyze = DeepFace.analyze(image,actions=['emotion']) 
        retr.append(analyze['dominant_emotion']) #here the first parameter is the image we want to analyze #the second one there is the action
    # print(analyze['dominant_emotion'])
    except:
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
        retr.append("sleepy")
    else:
        retr.append("not sleepy")
    return retr

if __name__ == "__main__":
    print(detect())
