from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')

image_path = 'image.jpeg'
results = model(image_path)

annotated_image = results[0].plot()
cv2.imshow('YOLOv8 Detection', annotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
