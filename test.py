# import the necessary packages
import numpy as np
import os
import cv2
import logging
import datetime
"""
Histogram Oriented Detection - academic paper on this available here:
https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf 

"""
FRAMERATE = 20
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()
if not os.path.isdir('./img'):
    os.mkdir('./img')

# open DroidCam video stream
cap = cv2.VideoCapture("http://192.168.0.122:4747/video")

out = cv2.VideoWriter(
    'stream.avi',
    cv2.VideoWriter_fourcc(*'MJPG'),
    FRAMERATE,
    (640,480))

while(True):
    ret, frame = cap.read()

    # 480p is a fine resolution
    frame = cv2.resize(frame, (640, 480))
    # Get it in grayscale 
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # detect people in the image
    # returns the bounding boxes for the detected objects
    boxes, weights = hog.detectMultiScale(frame, winStride=(12, 12))
    boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])

    for (xA, yA, xB, yB) in boxes:
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB),
                          (0, 255, 0), 2)
        cv2.imwrite(filename=f'./img/{datetime.datetime.now()}.png', img=frame)
    out.write(frame.astype('uint8'))
    cv2.imshow('Security Camera Feed', frame)
    
    # Checking to break out
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()

cv2.destroyAllWindows()
cv2.waitKey(1)