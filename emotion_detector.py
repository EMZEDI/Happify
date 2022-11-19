import cv2
from deepface import DeepFace
import numpy as np  #this will be used later in the process
import time

import cv2
cap = cv2.VideoCapture(0)
i = 0
while(True):
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

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
analyze = DeepFace.analyze(image,actions=['emotion'])  #here the first parameter is the image we want to analyze #the second one there is the action
print(analyze['dominant_emotion'])

