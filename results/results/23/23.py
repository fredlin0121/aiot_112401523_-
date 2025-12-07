from picamera2 import Picamera2
import cv2

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)}))
picam2.start()

ratio = 640 / 480
WIDTH = 400
HEIGHT = int(WIDTH / ratio)

bs = cv2.bgsegm.createBackgroundSubtractorGMG()

while True:
    frame = picam2.capture_array()
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.flip(frame, 1)

    gray = bs.apply(frame)
    mask = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=10)

    cnts, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in cnts:
        if cv2.contourArea(c) < 200:
            continue
        cv2.drawContours(frame, [c], -1, (0, 255, 255), 2)
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    combined = cv2.hconcat([frame, mask])
    cv2.imshow('frame', combined)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        picam2.stop()
        break
