import cv2
import numpy as np
import datetime

# Creating a VideoCapture object, passing in ip exactly as seen 
# in DroidCam app. 
FRAMERATE = 20
capture = cv2.VideoCapture("http://192.168.0.93:4747/video")
out = cv2.VideoWriter('stream.avi',cv2.VideoWriter_fourcc(*'MJPG'),FRAMERATE,(640,480))

# Repeatedly capturing frames on a loop, and showing
# them using imshow().

#brooklyn's copy
ret, frame1 = capture.read()
ret, frame2 = capture.read()

while capture.isOpened():
    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5),0)
    _,thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh,None,iterations=3)
    contours, _ = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    num_contours = 0
    for contour in contours: #loops through all detected motion 
        (x,y,w,h) = cv2.boundingRect(contour)
        if cv2.contourArea(contour) < 3000: #adds rectangle above a motion with a certain threshold of area
            continue
        cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        num_countours = num_contours+1
        
    cv2.putText(frame1, str(datetime.datetime.now()),(10,20),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),2)    
    cv2.imwrite(filename=f'./img/{datetime.datetime.now()}.png',img=frame1)
    out.write(frame1.astype('uint8'))
    
    cv2.imshow("feed",frame1)
    frame1 = frame2
    ret, frame2 = capture.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



capture.release()
out.release()
cv2.destroyAllWindows()


