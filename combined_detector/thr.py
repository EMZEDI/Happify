
import concurrent.futures
import logging
import queue
import random
import threading
import time

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

def producer(cap, fps, save_interval, event):
    """Pretend we're getting a number from the network.
    IN OUR CASE: it can be considered as running a while loop which does something and
    captures the picture
    """
    logging.info("started the producer")
    frame_count = 0
    while not event.is_set():
        while cap.isOpened():
            ret, frame = cap.read()
            logging.info("captured a frame of your face")
            logging.info(ret)
            if ret:
                frame_count += 1
                if frame_count % (fps * save_interval) == 0:
                    cv2.imwrite('image.jpg', frame)
                    logging.info("wrote the image to memory")
                    
                    # optional 
                    frame_count = 0
                
            # Break the loop
            else:
                break

        cap.release()
        cv2.destroyAllWindows()

        # TODO: Call the function which captures picture - done above
        logging.info("Captured a picture: %s", msg)
        # TODO: save the picture to the storage or the queue

        msg += 1

    logging.info("closing the capturing application")

def consumer(event):
    """Pretend we're saving a number in the database.
    IN OUR CASE: it can be considered as analyzing the 
    """
    logging.info("started the consumer")

    retr = []
    while not event.is_set():
        retr = []
        imgpath = 'image.jpg' 
        image = cv2.imread(imgpath)
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)   # needs to update for the consumer usage
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # needs to update
        logging.info("read the image to analyze")
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
        cv2.drawContours(image, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(image, [rightEyeHull], -1, (0, 255, 0), 1)

        #Detect if eye aspect ratio is less than threshold
        if(eyeAspectRatio < EYE_ASPECT_RATIO_THRESHOLD):
            retr.append("sleepy")
        else:
            retr.append("not sleepy")
        logging.log(retr)
        return retr

        # TODO: get the picture from the queue and analyze

        # message = the picture analysis
        # logging.info(
        #     "the picture has been sent to the front end with the attributes: %s (size=%d)", message, queue.qsize()
        # )

    logging.info("closing the report application")

if __name__ == "__main__":
    #Minimum threshold of eye aspect ratio below which alarm is triggered
    EYE_ASPECT_RATIO_THRESHOLD = 0.30

    #Minimum consecutive frames for which eye ratio is below threshold for alarm to be triggered
    EYE_ASPECT_RATIO_CONSEC_FRAMES = 10

    #COunts no. of consecutive frames below threshold value
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
    # start capturing
    cap = cv2.VideoCapture(0)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    save_interval = 2

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, cap, fps, save_interval, event)
        # time.sleep(2)
        executor.submit(consumer, event)

        time.sleep(1)
        logging.info("Main: about to set event")
        event.set()