from picamera2 import Picamera2
import cv2
import time

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

net = cv2.dnn.readNet(
    'opencv_face_detector.pbtxt',
    'opencv_face_detector_uint8.pb'
)

model = cv2.dnn_DetectionModel(net)
model.setInputParams(size=(300, 300), scale=1.0)

WIDTH = 600
FONT = cv2.FONT_HERSHEY_SIMPLEX

while True:
    begin_time = time.time()

    frame = picam2.capture_array()
    ratio = frame.shape[1] / frame.shape[0]
    HEIGHT = int(WIDTH / ratio)
    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    frame = cv2.flip(frame, 1)

    if frame.shape[2] == 4:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

    classes, confs, boxes = model.detect(frame, 0.5)
    for (classid, conf, box) in zip(classes, confs, boxes):
        x, y, w, h = box
        fps = 1 / (time.time() - begin_time)
        text = "fps: {:.1f} {:.2f}%".format(fps, float(conf) * 100)

        if y - 20 < 0:
            y1 = y + 20
        else:
            y1 = y - 10

        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)
        cv2.putText(frame, text, (x, y1), FONT, 0.5, (0, 204, 255), 2)

    cv2.imshow("video", frame)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        picam2.stop()
        break
