from picamera2 import Picamera2
import cv2
import numpy as np

RECT = ((220, 20), (370, 190))
(left, top), (right, bottom) = RECT

def roiarea(frame):
    return frame[top:bottom, left:right]

def replaceroi(frame, roi):
    frame[top:bottom, left:right] = roi
    return frame

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480), "format": "RGB888"})
picam2.configure(camera_config)
picam2.start()

WIDTH = 400
HEIGHT = 300

while True:
    frame = picam2.capture_array()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.flip(frame, 1)

    roi = roiarea(frame)
    roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    frame = replaceroi(frame, roi)

    cv2.rectangle(frame, RECT[0], RECT[1], (0, 0, 255), 2)
    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
picam2.stop()
