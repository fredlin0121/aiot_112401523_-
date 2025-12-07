from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')

image_path = 'image.jpeg'

results = model(image_path)

annotated_image = results[0].plot()

cv2.imwrite('detected_image.jpg', annotated_image)
print("Detection completed. Result saved as 'detected_image.jpg'.")
