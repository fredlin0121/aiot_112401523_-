import cv2
import numpy as np
from picamera2 import Picamera2

color = ((16, 59, 0), (47, 255, 255))
lower = np.array(color[0], dtype="uint8")
upper = np.array(color[1], dtype="uint8")

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
picam2.start()

WIDTH = 400
HEIGHT = int(WIDTH * (480 / 640))

while True:
    frame = picam2.capture_array()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.flip(frame, 1)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv = cv2.GaussianBlur(hsv, (11, 11), 0)

    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(cnt) < 100:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        p1 = (x - 2, y - 2)
        p2 = (x + w + 4, y + h + 4)
        cv2.rectangle(frame, p1, p2, (0, 255, 255), 2)

        out = cv2.bitwise_and(hsv, hsv, mask=mask)
        cv2.rectangle(hsv, p1, p2, (0, 255, 255), 2)
        cv2.rectangle(out, p1, p2, (0, 255, 255), 2)

        frame = cv2.hconcat([frame, hsv, out])

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
picam2.stop()
