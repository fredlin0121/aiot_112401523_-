import cv2
import numpy as np
import time
from picamera2 import Picamera2

def initNet():
    CONFIG = 'yolov4-tiny.cfg'
    WEIGHT = 'yolov4-tiny.weights'
    NAMES = 'coco.names'
    with open(NAMES, 'r') as f:
        names = [line.strip() for line in f.readlines()]
        colors = np.random.uniform(0, 255, size=(len(names), 3))
    net = cv2.dnn.readNet(CONFIG, WEIGHT)
    model = cv2.dnn_DetectionModel(net)
    model.setInputParams(size=(416, 416), scale=1/255.0)
    model.setInputSwapRB(True)
    return model, names, colors

def nnProcess(image, model):
    classes, confs, boxes = model.detect(image, 0.6, 0.3)
    return classes, confs, boxes

def drawBox(image, classes, confs, boxes, names, colors):
    new_image = image.copy()
    for (classid, conf, box) in zip(classes, confs, boxes):
        x, y, w, h = box
        label = '{}: {:.2f}'.format(names[int(classid)], float(conf))
        color = colors[int(classid)]
        cv2.rectangle(new_image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(new_image, label, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2
        )
    return new_image

model, names, colors = initNet()

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration(main={"size": (640, 480)})
picam2.configure(camera_config)
picam2.start()

WIDTH = 800
FONT = cv2.FONT_HERSHEY_SIMPLEX

while True:
    begin_time = time.time()

    frame = picam2.capture_array()
    ratio = frame.shape[1] / frame.shape[0]
    HEIGHT = int(WIDTH / ratio)
    frame = cv2.resize(frame, (WIDTH, HEIGHT))

    if frame.shape[2] == 4:
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

    classes, confs, boxes = nnProcess(frame, model)
    frame = drawBox(frame, classes, confs, boxes, names, colors)

    fps = 'fps: {:.2f}'.format(1 / (time.time() - begin_time))
    cv2.putText(frame, fps, (10, 30),
        FONT, 0.7, (0, 204, 255), 2
    )

    cv2.imshow('video', frame)

    if cv2.waitKey(1) == 27:
        cv2.destroyAllWindows()
        picam2.stop()
        break
