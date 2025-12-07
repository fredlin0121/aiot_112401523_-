from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')

image_paths = ['coin.jpg', 'image.jpeg']

for image_path in image_paths:
    results = model(image_path)
    annotated_image = results[0].plot()
    output_path = f'detected_{image_path}'
    cv2.imwrite(output_path, annotated_image)
    print(f"Detection completed. Result saved as {output_path}")
