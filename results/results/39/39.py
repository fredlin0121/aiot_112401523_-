from picamera2 import Picamera2, Preview
from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')

picam2 = Picamera2()
config = picam2.create_preview_configuration(main={"format": "RGB888", "size": (640, 480)})
picam2.configure(config)
picam2.start()

print("Press 'q' to quit")

try:
    while True:
        frame = picam2.capture_array()
        results = model(frame)
        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv8 Real-Time Detection", annotated_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    print("Program interrupted")

picam2.stop()
cv2.destroyAllWindows()
