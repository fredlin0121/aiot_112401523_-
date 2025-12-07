from ultralytics import YOLO
from picamera2 import Picamera2
import cv2

# Load YOLO model
model = YOLO("yolov8n.pt")

# Initialize PiCamera2
picam2 = Picamera2()
config = picam2.create_preview_configuration(
    main={"size": (640, 480), "format": "RGB888"}
)
picam2.configure(config)
picam2.start()

print("Camera started. Press 'q' to quit.")

while True:
    # Capture frame from PiCamera2 (RGB image)
    frame = picam2.capture_array()

    # Run YOLO inference (expects RGB)
    results = model(frame)

    # Plot results on frame
    annotated_frame = results[0].plot()

    # Convert to BGR for OpenCV display (optional, for correct colors)
    annotated_bgr = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)

    # Show frame
    cv2.imshow("YOLOv8 + PiCamera2", annotated_bgr)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
picam2.close()
