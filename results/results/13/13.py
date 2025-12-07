from picamera2 import Picamera2, Preview
import cv2
import numpy as np

ESC = 27
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

WIDTH = 400
HEIGHT = int(WIDTH * 480 / 640)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('video.mp4', fourcc, 30, (WIDTH, HEIGHT))

while True:
    frame = picam2.capture_array()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.flip(frame, 1)
    out.write(frame)

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ESC:
        break

picam2.stop()
out.release()
cv2.destroyAllWindows()