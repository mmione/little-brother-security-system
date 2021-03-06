import cv2
import numpy as np

# Creating a VideoCapture object, passing in ip exactly as seen 
# in DroidCam app. 
capture = cv2.VideoCapture("https://192.168.0.218:4343/mjpegfeed")

# Repeatedly capturing frames on a loop, and showing
# them using imshow().
while(True):
    ret, frame = capture.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()
