import numpy as np
import os
import cv2
import time
import yaml
import logging


"""
Histogram Oriented Detection - academic paper on this available here:
https://lear.inrialpes.fr/people/triggs/pubs/Dalal-cvpr05.pdf 

"""
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Load config - if not there, it returns a default value
config = {}
try:
    config = yaml.safe_load(open("config.yml", "r"))
except FileNotFoundError as e:
    logger.info(
        "Error: No config.yml found, using placeholder values, which will not work!"
    )


FRAMERATE = config.get("framerate", 20)
COOLDOWN = 10
IP = config.get("ip", "localhost")

hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

cv2.startWindowThread()
if not os.path.isdir("./img"):
    os.mkdir("./img")


def handler(cap):
    # We are going through frame by frame.
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
        # If we enter this for loop, something has been detected, whether or not its a false positive.
        # display the detected boxes in the colour picture
        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
        # cv2.imwrite(filename=f"./img/{datetime.datetime.now()}.png", img=frame)

    cv2.imshow("Security Camera Feed", frame)

    # Checking to break out

    return frame, boxes


def main():
    cap = cv2.VideoCapture(f"http://{IP}/mjpegfeed")
    out = cv2.VideoWriter(
        "stream.avi", cv2.VideoWriter_fourcc(*"MJPG"), FRAMERATE, (640, 480)
    )

    # Initializing of the control variables
    frame, hits = None, []
    record = False
    end = 0

    while True:
        logging.debug(f"Recording status: {str(record)}")
        if record and time.time() < end:
            out.write(frame.astype("uint8"))
        elif record and time.time() >= end:
            record = False
        frame, hits = handler(cap)
        if hits.size > 0:
            end = time.time() + COOLDOWN
            record = True

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    out.release()

    cv2.destroyAllWindows()
    cv2.waitKey(1)


if __name__ == "__main__":
    try:
        main()
    except cv2.error as e:
        logger.error("Encountered error with cv2, try rebooting Droidcam.")
        logger.error(str(e))
        exit(0)
